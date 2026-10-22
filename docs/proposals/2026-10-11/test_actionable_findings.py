"""N6: offline revision admission and actual findings artifact regressions."""
import base64
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_managed_summary import m, fixture, REQUEST, SUMMARY, REQ, NOW, HEAD, BASE


def change_request(body=""):
    return {"id": 900, "user": {"login": m.VERIFIER},
            "submitted_at": SUMMARY["created_at"], "commit_id": HEAD,
            "state": "CHANGES_REQUESTED", "body": body,
            "html_url": "https://github.com/404-ac-notfound/keystone-proof/pull/14#pullrequestreview-900"}


class ActionableFindings(unittest.TestCase):
    def run_poll(self, body="", summary=False, inline=None, inline_after=0):
        clock = [0]
        def sleep(seconds):
            clock[0] += seconds
        def api(path, **kwargs):
            if '/issues/14/comments?' in path:
                return [REQUEST, SUMMARY] if summary else [REQUEST]
            if '/pulls/14/reviews?' in path:
                return [change_request(body)]
            if '/pulls/14/comments?' in path:
                return [] if inline is None or clock[0] < inline_after else [{"id": 901, "user": {"login": m.VERIFIER},
                    "created_at": SUMMARY["created_at"], "original_commit_id": HEAD,
                    "body": inline, "html_url": "https://github.com/example#discussion_r901"}]
            if '/check-runs?' in path:
                return {"check_runs": []}
            raise AssertionError(path)
        c, _ = fixture()
        with tempfile.TemporaryDirectory() as temp, patch.object(m, 'api', side_effect=api), \
                patch.object(m, 'gates'), patch.object(m, 'current'), \
                patch.object(m, 'now_utc', return_value=NOW), \
                patch.object(m.time, 'monotonic', side_effect=lambda: clock[0]), \
                patch.object(m.time, 'sleep', side_effect=sleep), patch.object(m, 'emit') as emit:
            old = os.getcwd()
            try:
                os.chdir(temp)
                Path('out').mkdir()
                m.poll(c, REQ)
                result = copy.deepcopy(emit.call_args.args[0])
                findings = Path('out/findings.md').read_text()
            finally:
                os.chdir(old)
        return result, findings, clock[0]

    def test_empty_change_request_alone_never_admits_revision(self):
        for body in ('', ' \n\t'):
            with self.subTest(body=body):
                result, findings, elapsed = self.run_poll(body)
                self.assertEqual(result['verdict'], 'NO-VERDICT')
                self.assertEqual(findings, '')
                self.assertEqual(elapsed, 1800)

    def test_empty_change_request_beside_clean_summary_never_admits_revision(self):
        for body in ('', ' \n\t'):
            with self.subTest(body=body):
                result, findings, elapsed = self.run_poll(body, summary=True)
                self.assertEqual(result['verdict'], 'NO-VERDICT')
                self.assertEqual(findings, '')
                self.assertEqual(elapsed, 1800)

    def test_clean_text_change_request_cannot_supply_revision_material(self):
        for text in ('No issues found.', 'No findings.', 'No actionable findings.'):
            with self.subTest(text=text):
                result, findings, _ = self.run_poll(text, summary=True)
                self.assertEqual(result['verdict'], 'NO-VERDICT')
                self.assertEqual(findings, '')

    def test_late_inline_findings_remain_admissible_and_exclude_summary(self):
        text = '[P1] calc.py adds one extra: return a + b instead.'
        result, findings, elapsed = self.run_poll(summary=True, inline=text, inline_after=30)
        self.assertEqual(result['verdict'], 'REVIEW-WITH-FINDINGS')
        self.assertEqual(findings, text)
        self.assertEqual(elapsed, 90)
        self.assertNotIn(SUMMARY['body'], findings)

    def test_nonempty_prose_change_request_remains_admissible(self):
        text = 'Please remove the extra + 1 from calc.py so add returns a + b.'
        result, findings, elapsed = self.run_poll(text, summary=True)
        self.assertEqual(result['verdict'], 'REVIEW-WITH-FINDINGS')
        self.assertEqual(findings, text)
        self.assertEqual(elapsed, 60)

    def test_priority_only_header_only_sha_only_and_clean_inline_are_not_findings(self):
        for body in ('[P1]', 'Codex Review: Here are some suggestions', HEAD, 'No issues found.'):
            with self.subTest(body=body):
                self.assertEqual(m.actionable_findings([{
                    'kind': 'inline', 'body': body, 'bound_by': 'original_commit_id'}]), '')

    def test_summary_body_never_becomes_revision_material_from_priority_text(self):
        record = m.review_record('issue', SUMMARY, REQ, NOW)
        record['body'] += '\n[P1] summary annotation only'
        self.assertEqual(m.actionable_findings([record]), '')

    def run_prepare(self, records, supplied, admitted=True):
        c, _ = fixture()
        with tempfile.TemporaryDirectory() as temp, patch.object(m, 'gates'), \
                patch.object(m, 'current') as current, patch.object(m, 'api') as api:
            old = os.getcwd()
            try:
                os.chdir(temp)
                Path('.pilot/first').mkdir(parents=True)
                prior = {**REQ, 'verdict': 'REVIEW-WITH-FINDINGS', 'posts': records}
                Path('.pilot/first/verdict.json').write_text(json.dumps(prior))
                Path('.pilot/first/findings.md').write_text(supplied)
                Path('calc.py').write_text('unchanged sentinel')
                api.return_value = {'content': base64.b64encode(b'def add(a,b): return a+b+1\n').decode()}
                if admitted:
                    m.prepare(c, 2)
                    self.assertEqual(Path('.pilot/findings.md').read_text(), supplied.strip())
                    current.assert_called_once_with(c, REQ['pr'], HEAD, BASE)
                    api.assert_called_once()
                else:
                    with self.assertRaisesRegex(m.Stop, 'revision requires actionable|artifact mismatch'):
                        m.prepare(c, 2)
                    current.assert_not_called()
                    api.assert_not_called()
                    self.assertEqual(Path('calc.py').read_text(), 'unchanged sentinel')
                    self.assertFalse(Path('.pilot/findings.md').exists())
            finally:
                os.chdir(old)

    def test_prepare_rejects_empty_change_request_before_api_or_author_input(self):
        record = m.review_record('review', change_request(), REQ, NOW)
        self.run_prepare([record], '', admitted=False)

    def test_prepare_rejects_summary_only_feedback_before_api_or_author_input(self):
        records = [m.review_record('review', change_request(), REQ, NOW),
                   m.review_record('issue', SUMMARY, REQ, NOW)]
        self.run_prepare(records, SUMMARY['body'], admitted=False)

    def test_prepare_requires_artifact_to_match_bound_actionable_records(self):
        text = '[P1] Remove the extra + 1 from calc.py.'
        record = m.review_record('review', change_request(text), REQ, NOW)
        for supplied in ('', 'No issues found.', text + '\nadditional unbound instructions'):
            with self.subTest(supplied=supplied):
                self.run_prepare([record], supplied, admitted=False)

    def test_prepare_passes_exact_actionable_text(self):
        text = '[P1] Remove the extra + 1 from calc.py.'
        record = m.review_record('review', change_request(text), REQ, NOW)
        self.run_prepare([record], text)
