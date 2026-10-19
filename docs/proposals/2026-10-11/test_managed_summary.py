"""Captured live provider regression plus adversarial OFFLINE replay. No calls."""
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from test_managed_controller import m, fixture

CAPTURE = json.loads((Path(__file__).parent / "fixtures/managed-review-39227996178.json").read_text())
REQUEST, SUMMARY, CLEAN = CAPTURE
HEAD = "be0d22f3ab3aeb04cf31e63b131b5a22f7a80978"
BASE = "6f1ce8c93454fc535d4158dea093a8f0d1169461"
REQ = {"pr": "14", "head": HEAD, "base": BASE, "request_created_at": REQUEST["created_at"]}
NOW = dt.datetime(2026, 10, 19, 9, 15, tzinfo=dt.timezone.utc)


def state_post(**changes):
    post = copy.deepcopy(SUMMARY)
    state = {"code_review": {"commit_sha": HEAD, "has_any_findings": False,
                            "has_unresolved_findings": False, "status": "completed"},
             "security_review": dict.fromkeys(("commit_sha", "has_any_findings",
                                              "has_unresolved_findings", "status"))}
    state["code_review"].update(changes)
    post["body"] = "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 " + json.dumps(state) + " -->"
    return post


class ManagedSummary(unittest.TestCase):
    def verdict(self, post, req=REQ):
        return m.managed_summary(post, req, NOW)

    def test_exact_live_bytes_and_outcome(self):
        for post in CAPTURE:
            self.assertEqual(hashlib.sha256(post["body"].encode()).hexdigest(), post["body_sha256"])
        self.assertEqual(SUMMARY["body_sha256"], "be38bea9f65afb9dab76b1ed81ff074d598ef82d300de7cec784e042ab199fa2")
        record = m.review_record("issue", SUMMARY, REQ, NOW)
        self.assertEqual(record["bound_by"], "codex-review-state:v1")
        self.assertEqual(m.classify([record]), "REVIEW-CLEAN")
        self.assertIsNone(m.review_record("issue", CLEAN, REQ, NOW))

    def test_no_borrowing_full_sha_from_summary_for_short_prose(self):
        post = state_post(status="running")
        self.assertEqual(m.classify([m.review_record("issue", post, REQ, NOW)]), "NO-VERDICT")
        self.assertIsNone(m.bind("issue", CLEAN, HEAD, REQUEST["created_at"]))

    def test_wrong_full_sha_short_sha_and_missing_sha(self):
        for sha in (BASE, HEAD[:10], None, "", HEAD.upper()):
            with self.subTest(sha=sha):
                self.assertEqual(self.verdict(state_post(commit_sha=sha)), "NO-VERDICT")

    def test_boolean_types_and_inconsistent_flags(self):
        for field in ("has_any_findings", "has_unresolved_findings"):
            for value in (None, 0, 1, "false", [], {}):
                with self.subTest(field=field, value=value):
                    self.assertEqual(self.verdict(state_post(**{field: value})), "NO-VERDICT")
        self.assertEqual(self.verdict(state_post(has_unresolved_findings=True)), "NO-VERDICT")

    def test_findings_flags_require_actionable_bound_findings(self):
        record = m.review_record("issue", state_post(has_any_findings=True), REQ, NOW)
        self.assertEqual(m.classify([record]), "NO-VERDICT")
        inline = {"kind": "inline", "body": "[P1] Incorrect addition", "state": None}
        self.assertEqual(m.classify([record, inline]), "REVIEW-WITH-FINDINGS")

    def test_publisher_app_pr_and_comment_identity(self):
        changes = [{"user": {"login": "someone", "type": "Bot"}},
                   {"user": {"login": m.VERIFIER, "type": "User"}},
                   {"performed_via_github_app": {"id": 1}},
                   {"performed_via_github_app": None},
                   {"issue_url": f"https://api.github.com/repos/{m.REPO}/issues/13"},
                   {"issue_url": "https://api.github.com/repos/other/repo/issues/14"},
                   {"html_url": SUMMARY["html_url"] + "x"}, {"id": True}]
        for change in changes:
            with self.subTest(change=change):
                self.assertEqual(self.verdict({**SUMMARY, **change}), "NO-VERDICT")

    def test_timestamps_reject_old_missing_future_and_reversed_edits(self):
        changes = [{"created_at": "2026-10-19T09:11:09Z"}, {"created_at": None},
                   {"updated_at": None}, {"updated_at": "2026-10-19T09:11:25Z"},
                   {"updated_at": "2026-10-19T09:15:01Z"},
                   {"updated_at": "yesterday"}]
        for change in changes:
            with self.subTest(change=change):
                self.assertEqual(self.verdict({**SUMMARY, **change}), "NO-VERDICT")
        # Editing an old summary after our request does not establish creation.
        old = {**SUMMARY, "created_at": "2026-10-18T09:00:00Z"}
        self.assertEqual(self.verdict(old), "NO-VERDICT")

    def test_duplicate_keys_versions_markers_and_schema_changes(self):
        post = state_post()
        body = post["body"]
        bodies = [body.replace(':v1 ', ':v2 '), body + '\n' + body,
                  body.replace('"status": "completed"', '"status": "running", "status": "completed"'),
                  body.replace('"code_review":', '"other":'),
                  body.replace('"status": "completed"', '"status": "completed", "new_key": true'),
                  body.replace('"commit_sha": null', '"commit_sha": "' + HEAD + '"'),
                  body.replace('"status": "completed"', '"status": "completed",'),
                  body.replace('<!-- codex-pull-request-review-summary -->\n', '')]
        for value in bodies:
            with self.subTest(body=value):
                p = {**post, "body": value + '\nNo issues found. ' + HEAD}
                self.assertEqual(self.verdict(p), "NO-VERDICT")
                self.assertIsNone(m.bind("issue", p, HEAD, REQ["request_created_at"]))
                record = m.review_record("issue", p, REQ, NOW)
                self.assertEqual(m.classify([record]), "NO-VERDICT")

    def test_unaccepted_summary_vetoes_legacy_clean_but_findings_dominate(self):
        bad = m.review_record("issue", state_post(status="running"), REQ, NOW)
        clean = {"kind": "review", "body": "No issues found.", "state": "COMMENTED"}
        self.assertEqual(m.classify([bad, clean]), "NO-VERDICT")
        self.assertEqual(m.classify([bad, {**clean, "state": "CHANGES_REQUESTED"}]), "REVIEW-WITH-FINDINGS")

    def test_poll_emits_real_summary_receipt_and_excludes_short_sha(self):
        self.run_poll()

    def test_poll_resets_settle_time_after_incomplete_observation(self):
        self.run_poll(interrupt=True)

    def run_poll(self, interrupt=False):
        clock = [0]
        def sleep(seconds):
            clock[0] += seconds
        def api(path, **kwargs):
            if '/issues/14/comments?' in path:
                summary = state_post(status="running") if interrupt and clock[0] == 30 else SUMMARY
                return [REQUEST, summary, CLEAN]
            if '/reviews?' in path or '/pulls/14/comments?' in path:
                return []
            if '/check-runs?' in path:
                return {"check_runs": []}
            raise AssertionError(path)
        c, _ = fixture()
        with patch.object(m, 'api', side_effect=api), patch.object(m, 'gates'), \
                patch.object(m, 'current') as current, patch.object(m, 'now_utc', return_value=NOW), \
                patch.object(m.time, 'monotonic', side_effect=lambda: clock[0]), \
                patch.object(m.time, 'sleep', side_effect=sleep), patch.object(m, 'emit') as emit, \
                patch.object(m.Path, 'write_text'):
            m.poll(c, REQ)
        result = emit.call_args.args[0]
        self.assertEqual(result['verdict'], 'REVIEW-CLEAN')
        self.assertEqual([p['id'] for p in result['posts']], [SUMMARY['id']])
        self.assertEqual(clock[0], 120 if interrupt else 60)
        current.assert_called_with(c, REQ['pr'], HEAD, BASE)
