"""Offline regression tests; no GitHub calls or provider invocations."""
import contextlib
import importlib.util
import io
import json
import os
import pathlib
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
H1, H2 = "a" * 40, "b" * 40
LOGIN = "chatgpt-codex-connector[bot]"


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / ".github/scripts" / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


pv, wr = module("poll_verdict"), module("write_receipt")


def evidence(head=H1, verdict="REVIEW-CLEAN", ident="review:1"):
    return {"expected_head": head, "verdict": verdict, "verifier_login": LOGIN,
            "bound_by": ["commit_id"], "consumed_ids": [ident],
            "quoted": [{"id": ident, "login": LOGIN, "bound_by": "commit_id", "text": "No major issues"}],
            "observed_authors": [LOGIN], "waited_seconds": 1, "check_runs": [],
            "raw_observed": [], "reason": None}


def receipt(first, second=None, revised=False):
    env = {"ISSUE": "3", "PR": "4", "HEAD_1": H1, "HEAD_2": H2 if revised else "",
           "PR_HEAD_NOW": H2 if revised else H1, "VERIFIED_TESTS": "true",
           "RESULT_AUTHOR": "success", "RESULT_VERIFY1": "success",
           "RESULT_REVISE": "success" if revised else "skipped",
           "RESULT_VERIFY2": "success" if revised else "skipped",
           "VERDICT1": "REVIEW-WITH-FINDINGS" if revised else "REVIEW-CLEAN",
           "VERDICT2": "REVIEW-CLEAN" if revised else "", "VERIFIER_LOGIN": LOGIN}
    with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, env, clear=True):
        old = os.getcwd()
        os.chdir(d)
        try:
            for label, record in (("first", first), ("second", second)):
                if record is not None:
                    path = pathlib.Path(f"arts/verdict-{label}/verdict-{label}.json")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(record))
            with contextlib.redirect_stdout(io.StringIO()):
                wr.main()
            return pathlib.Path("jobs/3/receipt.md").read_text()
        finally:
            os.chdir(old)


class CorrectionTests(unittest.TestCase):
    def test_existing_binding_and_classifier_cases(self):
        namespace = runpy.run_path(str(ROOT / "tests_pilot/test_poll_verdict.py"))
        for name, fn in namespace.items():
            if name.startswith("test_"):
                with self.subTest(name=name):
                    fn()

    def test_old_review_cannot_override_binding_with_body_sha(self):
        self.assertIsNone(pv.bind("review", {"commit_id": H1, "body": f"Reviewed {H2}"}, H2, [H1]))

    def test_old_inline_cannot_override_binding_with_body_sha(self):
        self.assertIsNone(pv.bind("review_comment", {"original_commit_id": H1, "body": f"Reviewed {H2}"}, H2, [H1]))

    def test_bound_quota_or_status_message_is_not_findings(self):
        for text in ("Review limit reached", "Could not access repository", "Starting review"):
            with self.subTest(text=text):
                self.assertIsNone(pv.classify([{"kind": "issue_comment", "body": text}]))

    def test_clean_text_with_finding_is_findings(self):
        self.assertEqual(pv.classify([{"kind": "review", "body": "No major issues otherwise. [P1] Data loss"}]), "REVIEW-WITH-FINDINGS")

    def test_missing_artifact_fails(self):
        self.assertIn("**TRANSPORT:** TRANSPORT FAIL", receipt(None))

    def test_wrong_head_fails(self):
        self.assertIn("**TRANSPORT:** TRANSPORT FAIL", receipt(evidence(H2)))

    def test_wrong_verifier_fails(self):
        record = evidence()
        record["verifier_login"] = "someone-else"
        self.assertIn("**TRANSPORT:** TRANSPORT FAIL", receipt(record))

    def test_mismatched_verdict_fails(self):
        self.assertIn("**TRANSPORT:** TRANSPORT FAIL", receipt(evidence(verdict="NO-VERDICT")))

    def test_empty_bound_evidence_fails(self):
        record = evidence()
        record["consumed_ids"] = []
        self.assertIn("**TRANSPORT:** TRANSPORT FAIL", receipt(record))

    def test_clean_first_pass_records_unexercised_revision(self):
        result = receipt(evidence())
        self.assertIn("**TRANSPORT:** TRANSPORT PASS", result)
        self.assertIn("UNEXERCISED", result)

    def test_distinct_bound_second_review_passes(self):
        result = receipt(evidence(verdict="REVIEW-WITH-FINDINGS"), evidence(H2, ident="review:2"), True)
        self.assertIn("**TRANSPORT:** TRANSPORT PASS", result)

    def test_reused_second_review_fails(self):
        result = receipt(evidence(verdict="REVIEW-WITH-FINDINGS"), evidence(H2), True)
        self.assertIn("**TRANSPORT:** TRANSPORT FAIL", result)

    def test_failure_status_is_enforced_after_evidence_publication(self):
        workflow = (ROOT / ".github/workflows/k14-pilot.yml").read_text()
        self.assertIn("  checks: read", workflow)
        self.assertIn('SEEDED_ISSUE: "UNASSIGNED"', workflow)
        pos = workflow.index("      - name: Enforce transport outcome")
        self.assertGreater(pos, workflow.index('git push origin "HEAD:refs/heads/evidence/$ISSUE"'))
        script = "\n".join(line[10:] for line in workflow[pos:].split("        run: |\n", 1)[1].splitlines())
        for status, sha, expected in (("PASS", "receipt-sha", 0), ("FAIL", "receipt-sha", 1), ("PASS", "", 1), ("", "", 1)):
            with self.subTest(status=status, sha=sha):
                result = subprocess.run(["bash", "-c", script], env={"TRANSPORT": status, "RECEIPT_SHA": sha}, capture_output=True)
                self.assertEqual(result.returncode, expected)


if __name__ == "__main__":
    unittest.main()
