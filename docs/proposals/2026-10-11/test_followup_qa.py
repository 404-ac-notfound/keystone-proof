"""Realistic API shapes and malformed-config regressions; offline synthetic evidence."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from test_managed_controller import m, fixture, FakeAPI, A, NOW
from prepare_isolation_record import prepare
from k14_controller import Stop as HelperStop


class FollowupQA(unittest.TestCase):
    def test_jobs_pagination_produces_a_real_blocked_receipt_file(self):
        c, _ = fixture()
        pages = [{"total_count": 2, "jobs": [{"id": 1, "name": "guard", "conclusion": "success"}]},
                 {"total_count": 2, "jobs": [{"id": 2, "name": "author", "conclusion": "failure"}]}]
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"GITHUB_RUN_ID": "42", "GITHUB_SHA": A}), \
                patch.object(m.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout=json.dumps(pages))) as run:
            old = os.getcwd()
            try:
                os.chdir(d)
                m.receipt(c)
                receipt = json.loads(Path("out/receipt.json").read_text())
                self.assertEqual([j["id"] for j in receipt["jobs"]], [1, 2])
                self.assertEqual(receipt["outcome"], "BLOCKED")
                self.assertFalse(receipt["final_continuity_acceptance"]["build_complete"])
                self.assertTrue(Path("out/receipt.md").exists())
                self.assertIn("--slurp", run.call_args.args[0])
                self.assertIn("actions/runs/42/jobs?per_page=100", run.call_args.args[0][-1])
            finally:
                os.chdir(old)

    def test_list_endpoint_pages_still_flatten_and_malformed_pages_stop(self):
        with patch.object(m.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout='[[{"id":1}],[{"id":2}]]')):
            self.assertEqual(m.api('synthetic', paginate=True), [{"id": 1}, {"id": 2}])
        for payload in ({"jobs": []}, [None], [{"jobs": None}], [{"jobs": ["bad"]}], [["bad"]]):
            for page_key in (None, "jobs"):
                with self.subTest(payload=payload, key=page_key), \
                        patch.object(m.subprocess, "run", return_value=SimpleNamespace(returncode=0, stdout=json.dumps(payload))), \
                        self.assertRaises(m.Stop):
                    m.api('synthetic', paginate=True, page_key=page_key)

    def test_malformed_preflight_cli_emits_blocked_without_api_or_author(self):
        c, e = fixture()
        mutations = [None, [], 1]
        for key in ("environment", "old_oauth_retirement", "author_credential", "request_credential"):
            v = copy.deepcopy(c); v[key] = None; mutations.append(v)
        for value in (None, {}, [None, {}], [{"seat": []}, {"seat": "Kobe"}]):
            v = copy.deepcopy(c); v["independent_isolation"] = value; mutations.append(v)
        for kind in ("author_credential", "request_credential"):
            for field in ("retirement", "protected_environment", "revocation_bound"):
                v = copy.deepcopy(c); v[kind][field] = None; mutations.append(v)
        v = copy.deepcopy(c); v["owner_authorization"] = ["not an object"]; mutations.append(v)
        for value in mutations:
            with self.subTest(value=value), tempfile.TemporaryDirectory() as d, \
                    patch.dict(os.environ, {**e, "K14_PREFLIGHT_JSON": json.dumps(value)}), \
                    patch("sys.argv", ["controller", "author"]), patch.object(m, "api") as api, \
                    patch.object(m, "finish_author") as author, patch("builtins.print"):
                old = os.getcwd()
                try:
                    os.chdir(d)
                    self.assertEqual(m.main(), 1)
                    self.assertEqual(json.loads(Path("out/stop.json").read_text())["outcome"], "BLOCKED")
                    api.assert_not_called(); author.assert_not_called()
                finally:
                    os.chdir(old)

    def test_type_and_attribute_errors_are_sanitised_cli_blocked(self):
        c, e = fixture()
        for error in (TypeError('synthetic secret-like text'), AttributeError('synthetic secret-like text')):
            with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {**e, "K14_PREFLIGHT_JSON": json.dumps(c)}), \
                    patch("sys.argv", ["controller", "receipt"]), patch.object(m, "receipt", side_effect=error), \
                    patch("builtins.print"):
                old = os.getcwd()
                try:
                    os.chdir(d)
                    self.assertEqual(m.main(), 1)
                    stop = Path('out/stop.json').read_text()
                    self.assertNotIn('secret-like', stop)
                    self.assertEqual(json.loads(stop)['reason'], type(error).__name__)
                finally:
                    os.chdir(old)

    def test_headline_must_be_its_own_paragraph(self):
        c, _ = fixture()
        for tail in ('FAIL: withdrawn', 'PASS withdrawn.', 'different revision short-ref'):
            body = f'Urahara: PASS {A}\n{tail}'
            c['independent_isolation'][0]['comment_body_sha256'] = hashlib.sha256(body.encode()).hexdigest()
            api = FakeAPI(); api.isolation_overrides = {'body': body}
            with self.subTest(tail=tail), self.assertRaisesRegex(m.Stop, 'own paragraph'):
                m.verify_isolation_comments(c, A, api)

    def test_comment_helper_hashes_exact_bytes_and_validates_identity(self):
        url = 'https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-101'
        api = FakeAPI()
        body = f'Urahara: PASS {A}\r\n\r\nIndependent candidate isolation only.\r\n'
        api.isolation_overrides = {'body': body}
        record = prepare(url, 'Urahara', A, api)
        self.assertEqual(record['comment_body_sha256'], hashlib.sha256(body.encode()).hexdigest())
        self.assertNotEqual(record['comment_body_sha256'], hashlib.sha256(body.replace('\r\n','\n').encode()).hexdigest())
        self.assertEqual(len(api.calls), 1)
        self.assertEqual(api.calls[0][1], 'GET')
        with self.assertRaises(HelperStop):
            prepare(url, 'Kobe', A, api)
        with self.assertRaises(HelperStop):
            prepare(url.replace('keystone-proof','KEYSTONE'), 'Urahara', A, api)
