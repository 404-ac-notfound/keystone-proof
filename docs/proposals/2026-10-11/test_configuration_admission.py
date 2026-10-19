"""Offline one-time admission regressions; synthetic facts, no provider invocation."""
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_managed_controller import fixture, m, A, isolation_body
from prepare_launch_envelope import build
from k14_controller import Stop as HelperStop

NOW = dt.datetime(2026, 10, 19, 4, 0, tzinfo=dt.timezone.utc)
CHECKED = "2026-10-19T03:50:00Z"


def admitted_fixture():
    c, e = fixture()
    c.update(pilot_id=m.ADMISSION_PILOT, seed_issue=7,
             approved_expiry_ceiling=m.ADMISSION_STOP,
             environment={"status": "UNKNOWN", "evidence": "synthetic configuration only"},
             connected_user_access="UNKNOWN", preflight_completed_at="2026-10-19T03:55:00Z")
    c["configuration_admission"] = {
        "one_time": True, "owner_decision": m.ADMISSION_DECISION, "expires_at": m.ADMISSION_STOP,
        "repo_review_configuration": {"status": "CONFIGURATION_ONLY", "repository": m.REPO,
                                      "checked_at": CHECKED, "evidence": "synthetic"},
        "owner_app_installation_scope": {"status": "CONFIGURATION_ONLY", "repository": m.REPO,
            "checked_at": CHECKED, "evidence": "synthetic", "owner": "404-ac-notfound", "installation_id": 161479376}}
    c["independent_isolation"] = [
        {"seat": seat, "status": "PASS", "controller_sha": m.BASELINE_SHA,
         "evidence": f"https://github.com/{m.REPO}/pull/9#issuecomment-{values[0]}",
         "comment_body_sha256": values[1]} for seat, values in m.BASELINE_REVIEWS.items()]
    c["evidence_rule_delta_review"] = {
        "seat": "Kobe", "status": "PASS", "controller_sha": A,
        "evidence": f"https://github.com/{m.REPO}/pull/13#issuecomment-103",
        "comment_body_sha256": hashlib.sha256(isolation_body("Kobe", A).encode()).hexdigest()}
    for kind in ("author_credential", "request_credential"):
        c[kind].update(created_at=CHECKED, expires_at=m.ADMISSION_STOP, use_until=m.ADMISSION_STOP)
    e.update(K14_EXPIRES_AT=m.ADMISSION_STOP, K14_CASH_CHECKED_AT=CHECKED)
    return c, e


class ConfigurationAdmission(unittest.TestCase):
    def test_unknowns_are_preserved_and_no_provider_call_occurs(self):
        c, e = admitted_fixture()
        original = copy.deepcopy(c)
        with patch.object(m, "api") as api:
            self.assertEqual(m.gates(c, e, NOW), A)
            api.assert_not_called()
        self.assertEqual(c, original)
        self.assertEqual(c["environment"]["status"], "UNKNOWN")
        self.assertEqual(c["connected_user_access"], "UNKNOWN")

    def test_unknown_without_explicit_exception_still_stops(self):
        c, e = admitted_fixture(); del c["configuration_admission"]
        with self.assertRaisesRegex(m.Stop, "readiness UNKNOWN"):
            m.gates(c, e, NOW)

    def test_scope_authority_and_evidence_mutations_stop(self):
        mutations = [
            (("pilot_id",), "OTHER"), (("seed_issue",), 8),
            (("configuration_admission", "one_time"), False),
            (("configuration_admission", "owner_decision"), "unapproved"),
            (("configuration_admission", "expires_at"), "2026-10-22T00:00:00Z"),
            (("environment", "status"), "READY"), (("connected_user_access",), "VERIFIED"),
            (("configuration_admission", "owner_app_installation_scope", "owner"), "other"),
            (("configuration_admission", "owner_app_installation_scope", "installation_id"), 1),
            (("configuration_admission", "repo_review_configuration", "repository"), "other/repo"),
            (("configuration_admission", "repo_review_configuration", "status"), "VERIFIED"),
            (("configuration_admission", "repo_review_configuration", "evidence"), ""),
            (("configuration_admission", "repo_review_configuration", "checked_at"), "2026-10-18T12:56:00Z"),
            (("configuration_admission", "owner_app_installation_scope", "checked_at"), "2026-10-19T04:01:00Z"),
            (("preflight_completed_at",), m.PREFLIGHT_DEADLINE),
            (("preflight_completed_at",), "2026-10-19T04:01:00Z"),
            (("max_reviews",), 3), (("max_author_revisions",), 2),
            (("paid_review_credits",), "OFF_UNVERIFIED"),
        ]
        for keys, value in mutations:
            with self.subTest(keys=keys, value=value):
                c, e = admitted_fixture(); target = c
                for key in keys[:-1]: target = target[key]
                target[keys[-1]] = value
                with self.assertRaises(m.Stop): m.gates(c, e, NOW)

    def test_baseline_or_delta_cannot_be_substituted(self):
        for target, key, value in (("baseline", "controller_sha", A),
                ("baseline", "comment_body_sha256", "0" * 64),
                ("baseline", "evidence", f"https://github.com/{m.REPO}/pull/9#issuecomment-1"),
                ("delta", "controller_sha", m.BASELINE_SHA), ("delta", "seat", "Urahara"),
                ("delta", "status", "PENDING"), ("delta", "comment_body_sha256", None)):
            c, e = admitted_fixture()
            record = c["independent_isolation"][0] if target == "baseline" else c["evidence_rule_delta_review"]
            record[key] = value
            with self.subTest(target=target, key=key), self.assertRaises(m.Stop): m.gates(c, e, NOW)
        c, e = admitted_fixture(); del c["evidence_rule_delta_review"]
        with self.assertRaises(m.Stop): m.gates(c, e, NOW)

    def test_verifier_checks_baseline_then_new_exact_sha(self):
        c, _ = admitted_fixture()
        with patch.object(m, "verify_review_comments", return_value=[]) as verify:
            m.verify_isolation_comments(c, A)
        self.assertEqual(verify.call_args_list[0].args[:2], (c["independent_isolation"], m.BASELINE_SHA))
        self.assertEqual(verify.call_args_list[1].args[:2], ([c["evidence_rule_delta_review"]], A))

    def test_delta_raw_body_edit_and_wrong_publisher_stop(self):
        c, _ = admitted_fixture(); delta = c["evidence_rule_delta_review"]
        payload = {"id": 103, "issue_url": f"https://api.github.com/repos/{m.REPO}/issues/13",
                   "user": {"login": "404-ac-notfound"}, "body": isolation_body("Kobe", A)}
        self.assertEqual(len(m.verify_review_comments([delta], A, lambda p: payload)), 1)
        for key, value in (("body", payload["body"] + "edited"), ("user", {"login": "other"})):
            with self.subTest(key=key), self.assertRaises(m.Stop):
                m.verify_review_comments([delta], A, lambda p: {**payload, key: value})

    def test_expiry_cannot_extend_and_running_checks_stop_at_hard_stop(self):
        c, e = admitted_fixture(); e["K14_EXPIRES_AT"] = "2026-10-20T00:00:00Z"
        with self.assertRaises(m.Stop): m.gates(c, e, NOW)
        c, e = admitted_fixture()
        with self.assertRaises(m.Stop): m.gates(c, e, m.utc(m.ADMISSION_STOP))

    def test_preflight_deadline_does_not_cut_off_already_green_runtime(self):
        c, e = admitted_fixture()
        later = dt.datetime(2026, 10, 19, 8, 30, tzinfo=dt.timezone.utc)
        e["K14_CASH_CHECKED_AT"] = "2026-10-19T07:30:00Z"
        for fact in c["configuration_admission"].values():
            if isinstance(fact, dict): fact["checked_at"] = e["K14_CASH_CHECKED_AT"]
        self.assertEqual(m.gates(c, e, later), A)

    def test_helper_stamps_only_successful_envelope_before_deadline(self):
        c, _ = admitted_fixture(); original = copy.deepcopy(c)
        values = build(c, A, m.ADMISSION_STOP, CHECKED, 125, True, NOW)
        result = json.loads(values["K14_PREFLIGHT_JSON"])
        self.assertEqual(c, original)
        self.assertEqual(result["preflight_completed_at"], "2026-10-19T04:00:00Z")
        self.assertEqual(result["environment"]["status"], "UNKNOWN")
        with self.assertRaisesRegex(HelperStop, "deadline"):
            build(c, A, m.ADMISSION_STOP, CHECKED, 125, True, m.utc(m.PREFLIGHT_DEADLINE))

    def test_access_runtime_errors_stay_blocked_and_receipt_preserves_unknowns(self):
        c, e = admitted_fixture()
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {**e, "K14_PREFLIGHT_JSON": json.dumps(c)}), \
                patch("sys.argv", ["controller", "receipt"]), patch.object(m, "receipt", side_effect=OSError("private")), \
                patch("builtins.print"):
            old = os.getcwd()
            try:
                os.chdir(d); self.assertEqual(m.main(), 1)
                stopped = json.loads(Path("out/stop.json").read_text())
                self.assertEqual(stopped["outcome"], "BLOCKED")
                self.assertNotIn("private", json.dumps(stopped))
            finally: os.chdir(old)
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"GITHUB_RUN_ID": "42", "GITHUB_SHA": A}), \
                patch.object(m, "api", return_value=[]):
            old = os.getcwd()
            try:
                os.chdir(d); m.receipt(c)
                result = json.loads(Path("out/receipt.json").read_text())
                self.assertEqual(result["outcome"], "BLOCKED")
                self.assertEqual(result["environment"]["status"], "UNKNOWN")
                self.assertEqual(result["connected_user_access"], "UNKNOWN")
                self.assertEqual(result["evidence_rule_delta_review"], c["evidence_rule_delta_review"])
            finally: os.chdir(old)
