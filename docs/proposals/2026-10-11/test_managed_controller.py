"""Offline behavioral tests. Synthetic evidence ONLY; no isolation assessment."""
import copy
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("controller", ROOT / "k14_controller.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
A, B = "a" * 40, "b" * 40
NOW = dt.datetime(2026, 10, 11, 1, 15, tzinfo=dt.timezone.utc)
STAMP = "2026-10-11T01:15:00Z"
EXPIRES = "2026-10-11T03:15:00Z"


def fixture():
    c = json.loads((ROOT / "pilot-config.json").read_text())
    c.update(pilot_id="SYNTHETIC_TEST_ONLY", seed_issue=9, approved_expiry_ceiling=EXPIRES,
             owner_authorization={"source": "synthetic receipt", "quote": "synthetic assent", "approved_sha": A},
             environment={"status": "READY", "evidence": "synthetic"}, connected_user_access="VERIFIED",
             managed_review_configuration="VERIFIED", paid_review_credits="OFF_VERIFIED",
             old_oauth_retirement={"secret_absence": "VERIFIED", "issuer_revocation": "VERIFIED", "evidence": "synthetic"},
             independent_isolation=[{"seat": seat, "status": "PASS", "controller_sha": A, "evidence": "synthetic"}
                                    for seat in ("Urahara", "Kobe")],
             author_credential={"fresh": True, "created_at": STAMP, "expires_at": EXPIRES,
                                "use_until": EXPIRES, "evidence": "synthetic"},
             request_credential={"created_at": STAMP, "expires_at": EXPIRES,
                                 "use_until": EXPIRES, "evidence": "synthetic"})
    for kind, name in (("author_credential", "k14-author-owner-approved"),
                       ("request_credential", "k14-review-owner-approved")):
        c[kind]["protected_environment"] = {"name": name, "status": "VERIFIED", "environment_only": True,
                                             "deployment_branch": "main", "unattended_policy": "VERIFIED", "evidence": "synthetic"}
        c[kind]["retirement"] = {"owner": "404-ac-notfound", "on_terminal": True,
                                  "on_cancel": True, "evidence": "synthetic"}
    e = {"GH_REPO": m.REPO, "GITHUB_RUN_ATTEMPT": "1", "GITHUB_SHA": A,
         "K14_APPROVED_SHA": A, "K14_ENABLED": "true", "K14_EXPIRES_AT": EXPIRES,
         "K14_CASH_CHECKED_AT": STAMP, "K14_CASH_STOP_VERIFIED": "true", "K14_INCLUDED_MINUTES": "125"}
    return c, e


class FakeAPI:
    def __init__(self):
        self.p = {"state": "open", "head": {"ref": "job/9", "sha": A, "repo": {"full_name": m.REPO}},
                  "base": {"ref": "main", "sha": B, "repo": {"full_name": m.REPO}}}
        self.files = [{"filename": "calc.py", "additions": 1, "deletions": 1, "patch": "diff"}]
        self.diff = "diff"
        self.refs = {}
        self.calls = []
        self.comments = []
        self.post_login = "404-ac-notfound"
        self.reviews = []
        self.inline = []
        self.after_current = None
        self.current_reads = 0

    def __call__(self, path, method="GET", payload=None, token=None, paginate=False, raw=False):
        self.calls.append((path, method, payload, token))
        if path.endswith("/git/refs"):
            if payload["ref"] in self.refs:
                raise m.Stop("slot already consumed")
            self.refs[payload["ref"]] = payload["sha"]
            return {"ref": payload["ref"]}
        if "/git/ref/" in path:
            ref = "refs/" + path.split("/git/ref/")[1]
            return {"object": {"sha": self.refs[ref]}}
        if "/files?" in path:
            return self.files
        if path.endswith("/pulls/7"):
            if raw:
                return self.diff
            self.current_reads += 1
            if self.after_current:
                self.after_current(self)
            return copy.deepcopy(self.p)
        if "/issues/7/comments" in path:
            if method == "POST":
                value = {"id": 100, "user": {"login": self.post_login}, "created_at": STAMP,
                         "body": payload["body"], "html_url": "https://example.invalid/synthetic"}
                self.comments.append(value)
                return value
            return self.comments
        if "/pulls/7/reviews" in path:
            return self.reviews
        if "/pulls/7/comments" in path:
            return self.inline
        if "/check-runs" in path:
            return {"check_runs": []}
        raise AssertionError("unexpected mocked endpoint: " + path)


class Gates(unittest.TestCase):
    def test_valid_synthetic(self):
        c, e = fixture()
        self.assertEqual(m.gates(c, e, NOW), A)

    def test_missing_runtime_gates(self):
        for key in fixture()[1]:
            with self.subTest(key=key):
                c, e = fixture()
                del e[key]
                with self.assertRaises(m.Stop):
                    m.gates(c, e, NOW)

    def test_runtime_mutations(self):
        values = {"GH_REPO": "someone/fork", "GITHUB_RUN_ATTEMPT": "2", "K14_APPROVED_SHA": B,
                  "K14_ENABLED": "false", "K14_EXPIRES_AT": "2030-01-01T00:00:00Z",
                  "K14_CASH_CHECKED_AT": "2026-10-11T01:16:00Z", "K14_INCLUDED_MINUTES": "124"}
        for key, value in values.items():
            with self.subTest(key=key):
                c, e = fixture()
                e[key] = value
                with self.assertRaises(m.Stop):
                    m.gates(c, e, NOW)

    def test_expiry_boundaries(self):
        c, e = fixture()
        for value in ("garbage", "2026-10-11T01:15:00Z", "2026-10-11T00:15:00Z"):
            with self.subTest(expiry=value), self.assertRaises(m.Stop):
                m.gates(c, {**e, "K14_EXPIRES_AT": value}, NOW)

    def test_thirty_day_pat_can_outlive_october_pilot(self):
        c, e = fixture()
        c["approved_expiry_ceiling"] = e["K14_EXPIRES_AT"] = m.PILOT_CEILING
        for kind in ("author_credential", "request_credential"):
            c[kind].update(use_until=m.PILOT_CEILING, expires_at="2026-11-10T01:15:00Z")
        self.assertEqual(m.gates(c, e, NOW), A)

    def test_pat_lifetime_measured_from_issuance_not_invocation(self):
        for issued, expiry in (("2026-10-01T01:15:00Z", "2026-10-31T01:15:00Z"),
                               (STAMP, "2026-11-10T01:15:00Z")):
            with self.subTest(issued=issued):
                c, e = fixture()
                c["request_credential"].update(created_at=issued, expires_at=expiry)
                self.assertEqual(m.gates(c, e, NOW), A)
                c["request_credential"]["expires_at"] = (
                    m.utc(expiry) + dt.timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
                with self.assertRaisesRegex(m.Stop, "30 days from issuance"):
                    m.gates(c, e, NOW)

    def test_invalid_credential_clocks_stop(self):
        for kind in ("author_credential", "request_credential"):
            for key, value in (("created_at", None), ("created_at", "2026-10-11T01:15:01Z"),
                               ("expires_at", None), ("expires_at", STAMP),
                               ("expires_at", "2026-10-11T03:14:59Z"),
                               ("use_until", None), ("use_until", STAMP),
                               ("use_until", "2026-10-11T03:15:01Z")):
                with self.subTest(kind=kind, key=key, value=value), self.assertRaises(m.Stop):
                    c, e = fixture()
                    c[kind][key] = value
                    m.gates(c, e, NOW)

    def test_earlier_credential_use_deadline_stops_at_boundary(self):
        c, e = fixture()
        c["request_credential"]["use_until"] = "2026-10-11T02:15:00Z"
        self.assertEqual(m.gates(c, e, NOW), A)
        with self.assertRaises(m.Stop):
            m.gates(c, e, m.utc(c["request_credential"]["use_until"]))

    def test_october_ceiling_cannot_be_extended_by_config(self):
        c, e = fixture()
        c["approved_expiry_ceiling"] = e["K14_EXPIRES_AT"] = "2026-10-23T00:00:01Z"
        with self.assertRaisesRegex(m.Stop, "23 October ceiling"):
            m.gates(c, e, NOW)
        c["approved_expiry_ceiling"] = "2026-10-23T00:00:01Z"
        e["K14_EXPIRES_AT"] = EXPIRES
        with self.assertRaises(m.Stop):
            m.gates(c, e, NOW)

    def test_missing_or_unowned_retirement_plan_stops(self):
        for kind in ("author_credential", "request_credential"):
            for key, value in (("owner", "Magic"), ("evidence", None),
                               ("on_terminal", False), ("on_cancel", False)):
                with self.subTest(kind=kind, key=key), self.assertRaises(m.Stop):
                    c, e = fixture()
                    c[kind]["retirement"][key] = value
                    m.gates(c, e, NOW)

    def test_pending_evidence(self):
        mutations = [lambda c: c.update(owner_authorization=None),
                     lambda c: c.update(seed_issue=1), lambda c: c.update(pilot_id="UNASSIGNED"),
                     lambda c: c["environment"].update(status="UNKNOWN"),
                     lambda c: c.update(connected_user_access="UNKNOWN"),
                     lambda c: c.update(paid_review_credits="OFF_UNVERIFIED"),
                     lambda c: c["old_oauth_retirement"].update(issuer_revocation="UNKNOWN"),
                     lambda c: c["author_credential"].update(fresh=False),
                     lambda c: c.update(max_reviews=3),
                     lambda c: c["independent_isolation"][0].update(status="PENDING"),
                     lambda c: c["independent_isolation"][1].update(controller_sha=B),
                     lambda c: c.update(controller_author="Kobe")]
        for i, mutate in enumerate(mutations):
            with self.subTest(case=i):
                c, e = fixture()
                mutate(c)
                with self.assertRaises(m.Stop):
                    m.gates(c, e, NOW)

    def test_green_main_cannot_replace_missing_isolation(self):
        c, e = fixture()
        c["independent_isolation"] = []
        c["keystone_green_main"] = {"status": "PASS", "sha": B, "evidence": "synthetic"}
        with self.assertRaisesRegex(m.Stop, "isolation PASS required"):
            m.gates(c, e, NOW)

    def test_green_main_cannot_replace_final_sha_rechecks(self):
        c, e = fixture()
        # Synthetic installation changed main's launch SHA from A to B.
        e.update(GITHUB_SHA=B, K14_APPROVED_SHA=B)
        c["owner_authorization"]["approved_sha"] = B
        c["keystone_green_main"] = {"status": "PASS", "sha": B, "evidence": "synthetic"}
        for rechecked_count in range(3):
            with self.subTest(rechecked=rechecked_count):
                for i, receipt in enumerate(c["independent_isolation"]):
                    receipt["controller_sha"] = B if i < rechecked_count else A
                if rechecked_count == 2:
                    self.assertEqual(m.gates(c, e, NOW), B)
                else:
                    with self.assertRaisesRegex(m.Stop, "isolation PASS required"):
                        m.gates(c, e, NOW)

    def test_default_config_is_unlaunchable(self):
        c = json.loads((ROOT / "pilot-config.json").read_text())
        with self.assertRaises(m.Stop):
            m.gates(c, fixture()[1], NOW)

    def test_environment_secret_fallback_or_unprotected_deployment_stops(self):
        for kind in ("author_credential", "request_credential"):
            for key, value in (("status", "UNAVAILABLE"), ("environment_only", False), ("deployment_branch", "*"),
                               ("unattended_policy", "UNVERIFIED"), ("name", "wrong"), ("evidence", None)):
                with self.subTest(credential=kind, field=key), self.assertRaises(m.Stop):
                    c, e = fixture()
                    c[kind]["protected_environment"][key] = value
                    m.gates(c, e, NOW)


class Transport(unittest.TestCase):
    def setUp(self):
        self.c, _ = fixture()
        self.api = FakeAPI()

    def claim(self, look=1):
        return m.reserve(self.c, look, 7, A, B, "42", self.api)

    def test_seed_launch_and_duplicate_label(self):
        c, e = fixture()
        self.api.refs["refs/heads/main"] = A
        event = {"action": "labeled", "label": {"name": "ready"},
                 "sender": {"login": "404-ac-notfound"}, "issue": {"number": 9}}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "event.json"
            path.write_text(json.dumps(event))
            with patch.dict(os.environ, {**e, "GITHUB_EVENT_PATH": str(path)}), \
                    patch.object(m, "api", self.api), patch.object(m, "emit") as emit, \
                    patch.object(m, "now_utc", return_value=NOW):
                m.guard(c)
                self.assertEqual(emit.call_args.args[0]["admitted"], "true")
                with self.assertRaises(m.Stop):
                    m.guard(c)

    def test_stale_candidate_receipts_stop_launch_before_any_api_call(self):
        c, e = fixture()
        e.update(GITHUB_SHA=B, K14_APPROVED_SHA=B)
        c["owner_authorization"]["approved_sha"] = B
        c["keystone_green_main"] = {"status": "PASS", "sha": B, "evidence": "synthetic"}
        with patch.dict(os.environ, e), patch.object(m, "api", self.api), \
                patch.object(m, "now_utc", return_value=NOW):
            with self.assertRaisesRegex(m.Stop, "isolation PASS required"):
                m.guard(c)
        self.assertEqual(self.api.calls, [])

    def test_final_sha_rechecks_allow_only_that_main_revision(self):
        c, e = fixture()
        e.update(GITHUB_SHA=B, K14_APPROVED_SHA=B)
        c["owner_authorization"]["approved_sha"] = B
        for receipt in c["independent_isolation"]:
            receipt["controller_sha"] = B
        event = {"action": "labeled", "label": {"name": "ready"},
                 "sender": {"login": "404-ac-notfound"}, "issue": {"number": 9}}
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "event.json"
            path.write_text(json.dumps(event))
            for main_sha in (A, B):
                self.api = FakeAPI()
                self.api.refs["refs/heads/main"] = main_sha
                with self.subTest(main=main_sha), \
                        patch.dict(os.environ, {**e, "GITHUB_EVENT_PATH": str(path)}), \
                        patch.object(m, "api", self.api), patch.object(m, "emit") as emit, \
                        patch.object(m, "now_utc", return_value=NOW):
                    if main_sha == B:
                        m.guard(c)
                        self.assertEqual(emit.call_args.args[0]["base"], B)
                        self.assertEqual(self.api.refs["refs/heads/job/9"], B)
                    else:
                        with self.assertRaisesRegex(m.Stop, "main moved"):
                            m.guard(c)
                        self.assertNotIn("refs/heads/job/9", self.api.refs)
                        emit.assert_not_called()

    def test_wrong_launch_sender_seed_and_activity_stop_before_claim(self):
        c, e = fixture()
        for change in ({"sender": {"login": "github-actions[bot]"}}, {"issue": {"number": 1}},
                       {"action": "opened"}, {"issue": {"number": 9, "pull_request": {"url": "synthetic"}}}):
            event = {"action": "labeled", "label": {"name": "ready"},
                     "sender": {"login": "404-ac-notfound"}, "issue": {"number": 9}, **change}
            with self.subTest(event=event), tempfile.TemporaryDirectory() as d:
                path = Path(d) / "event.json"
                path.write_text(json.dumps(event))
                with patch.dict(os.environ, {**e, "GITHUB_EVENT_PATH": str(path)}), \
                        patch.object(m, "api", self.api), patch.object(m, "now_utc", return_value=NOW):
                    with self.assertRaises(m.Stop):
                        m.guard(c)
                    self.assertFalse(self.api.calls)

    def test_global_slots_consumed_even_without_post(self):
        self.claim(1)
        self.claim(2)
        for look in (1, 2, 3):
            with self.subTest(look=look), self.assertRaises(m.Stop):
                self.claim(look)
        self.assertFalse(self.api.comments)

    def test_caps_stop_before_claim(self):
        cases = [(51, 1, True, "diff"), (1, 1001, True, "diff"), (1, 1, False, "diff"), (1, 1, True, "x" * 131073)]
        for count, lines, patch_present, diff in cases:
            self.api = FakeAPI()
            self.api.files = [{"additions": lines, "deletions": 0, **({"patch": "diff"} if patch_present else {})}] * count
            self.api.diff = diff
            with self.subTest(count=count, lines=lines, patch=patch_present), self.assertRaises(m.Stop):
                self.claim()
            self.assertFalse(self.api.refs)

    def test_exact_cap_boundaries(self):
        m.caps([{"additions": 20, "deletions": 0, "patch": "diff"}] * 50, "x" * 131072)

    def test_closed_fork_wrong_branch_and_stale(self):
        mutations = [lambda p: p.update(state="closed"), lambda p: p["head"]["repo"].update(full_name="someone/fork"),
                     lambda p: p["head"].update(ref="job/1"), lambda p: p["head"].update(sha=B),
                     lambda p: p["base"].update(sha=A)]
        for i, mutate in enumerate(mutations):
            self.api = FakeAPI()
            mutate(self.api.p)
            with self.subTest(case=i), self.assertRaises(m.Stop):
                self.claim()
            self.assertFalse(self.api.refs)

    def test_only_post_gets_request_token_and_duplicate_stops(self):
        claim = self.claim()
        result = m.request(self.c, claim, "SYNTHETIC_TOKEN", "42", self.api)
        self.assertEqual(result["request_id"], "100")
        token_calls = [c for c in self.api.calls if c[3]]
        self.assertEqual(len(token_calls), 1)
        self.assertEqual(token_calls[0][1], "POST")
        with self.assertRaises(m.Stop):
            m.request(self.c, claim, "SYNTHETIC_TOKEN", "42", self.api)
        self.assertEqual(len(self.api.comments), 1)

    def test_missing_token_cross_run_and_bad_claim(self):
        claim = self.claim()
        for token, run, edit in ((None, "42", {}), ("SYNTHETIC", "43", {}), ("SYNTHETIC", "42", {"look": 3})):
            with self.subTest(run=run, edit=edit), self.assertRaises(m.Stop):
                m.request(self.c, {**claim, **edit}, token, run, self.api)
        self.assertFalse(self.api.comments)

    def test_wrong_sender_no_retry(self):
        claim = self.claim()
        self.api.post_login = "github-actions[bot]"
        with self.assertRaises(m.Stop):
            m.request(self.c, claim, "SYNTHETIC", "42", self.api)
        with self.assertRaises(m.Stop):
            self.claim()

    def test_move_after_post_blocks(self):
        claim = self.claim()
        def move(api):
            if api.comments:
                api.p["head"]["sha"] = B
        self.api.after_current = move
        with self.assertRaisesRegex(m.Stop, "STALE"):
            m.request(self.c, claim, "SYNTHETIC", "42", self.api)


class Verdict(unittest.TestCase):
    def post(self, **kwargs):
        return {"user": {"login": m.VERIFIER}, "submitted_at": STAMP, "commit_id": A,
                "state": "COMMENTED", "body": "No issues found.", **kwargs}

    def test_structured_binding(self):
        self.assertEqual(m.bind("review", self.post(), A, STAMP), "commit_id")

    def test_wrong_actor_old_review_wrong_head_never_bind(self):
        for p in (self.post(user={"login": "github-actions[bot]"}), self.post(submitted_at="2026-10-10T00:00:00Z"),
                  self.post(commit_id=B, body=A), self.post(state="DISMISSED"), self.post(submitted_at=None)):
            with self.subTest(post=p):
                self.assertIsNone(m.bind("review", p, A, STAMP))

    def test_full_sha_required_for_unstructured_post(self):
        p = {"user": {"login": m.VERIFIER}, "created_at": STAMP, "body": "No issues found at " + A}
        self.assertEqual(m.bind("issue", p, A, STAMP), "full_reviewed_sha")
        self.assertIsNone(m.bind("issue", {**p, "body": A[:7]}, A, STAMP))

    def test_error_empty_or_status_not_clean(self):
        for body in ("", "Quota exceeded", "Create an environment", "review is running"):
            with self.subTest(body=body):
                self.assertEqual(m.classify([{"kind": "review", "body": body}]), "NO-VERDICT")

    def test_findings_dominate_clean(self):
        self.assertEqual(m.classify([{"kind": "review", "body": "No issues found."},
                                     {"kind": "inline", "body": "P1: defect"}]), "REVIEW-WITH-FINDINGS")

    def test_poll_rechecks_head_after_receiving_clean_verdict(self):
        c, e = fixture()
        api = FakeAPI()
        api.reviews = [dict(self.post(), id=200)]
        api.after_current = lambda a: a.p["head"].update(sha=B) if a.current_reads >= 3 else None
        tick = iter(range(0, 5000, 45))
        request = {"pr": "7", "head": A, "base": B, "request_created_at": STAMP}
        with patch.dict(os.environ, e), patch.object(m, "api", api), patch.object(m, "now_utc", return_value=NOW), \
                patch.object(m.time, "monotonic", side_effect=lambda: next(tick)), patch.object(m.time, "sleep"), \
                patch.object(m, "emit") as emit:
            with self.assertRaisesRegex(m.Stop, "STALE"):
                m.poll(c, request)
            emit.assert_not_called()

    def test_poll_timeout_keeps_no_verdict(self):
        c, e = fixture()
        api = FakeAPI()
        tick = iter(range(0, 10000, 600))
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, e), patch.object(m, "api", api), \
                patch.object(m, "now_utc", return_value=NOW), patch.object(m.time, "monotonic", side_effect=lambda: next(tick)), \
                patch.object(m.time, "sleep"), patch.object(m, "emit") as emit:
            old = os.getcwd()
            try:
                os.chdir(d)
                Path("out").mkdir()
                m.poll(c, {"pr": "7", "head": A, "base": B, "request_created_at": STAMP})
            finally:
                os.chdir(old)
            self.assertEqual(emit.call_args.args[0]["verdict"], "NO-VERDICT")


class Workflow(unittest.TestCase):
    def test_same_run_job_dependencies_and_secret_boundaries(self):
        w = yaml.load((ROOT / "k14-managed.yml.disabled").read_text(), Loader=yaml.BaseLoader)
        jobs = w["jobs"]
        self.assertEqual(w["on"], {"issues": {"types": ["labeled"]}})
        self.assertEqual(w["permissions"], {})
        self.assertEqual(jobs["request1"]["needs"], ["claim1"])
        self.assertEqual(jobs["verify1"]["needs"], ["request1"])
        self.assertEqual(jobs["request2"]["needs"], ["claim2"])
        self.assertEqual(jobs["verify2"]["needs"], ["request2"])
        self.assertIn("REVIEW-WITH-FINDINGS", jobs["revise"]["if"])
        self.assertEqual(jobs["receipt"]["needs"], list(jobs)[:-1])
        self.assertLessEqual(sum(int(j["timeout-minutes"]) for j in jobs.values()), 125)
        for name, j in jobs.items():
            with self.subTest(job=name):
                self.assertEqual(j["runs-on"], "ubuntu-24.04")
                self.assertIn('test "${ImageVersion:-}" = 20261004.327.1', j["steps"][0]["run"])
                self.assertNotIn("uses", j["steps"][0])
                if name in ("request1", "request2", "verify1", "verify2", "author", "revise", "finalcheck", "receipt"):
                    self.assertEqual(set(j["permissions"].values()), {"read"})
                request_secret = "secrets.K14_REVIEW_REQUEST_TOKEN" in json.dumps(j)
                self.assertEqual(request_secret, name in ("request1", "request2"))
                oauth_secret = "secrets.K14_AUTHOR_OAUTH_TOKEN" in json.dumps(j)
                self.assertEqual(oauth_secret, name in ("author", "revise"))
                if oauth_secret:
                    self.assertEqual(j["environment"], "k14-author-owner-approved")
                if request_secret:
                    self.assertEqual(j["environment"], "k14-review-owner-approved")
                for s in j["steps"]:
                    if "uses" in s:
                        self.assertRegex(s["uses"], r"@[0-9a-f]{40}$")
                    if "checkout@" in s.get("uses", ""):
                        self.assertEqual(s["with"]["ref"], "${{ github.sha }}")
                        self.assertEqual(s["with"]["persist-credentials"], "false")

    def test_receipt_does_not_fabricate_final_pass(self):
        c, _ = fixture()
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"GITHUB_RUN_ID": "42", "GITHUB_SHA": A}), \
                patch.object(m, "api", return_value=[]), patch.object(m, "emit") as emit:
            old = os.getcwd()
            try:
                os.chdir(d)
                Path("out").mkdir()
                m.receipt(c)
            finally:
                os.chdir(old)
            self.assertEqual(emit.call_args.args[0]["outcome"], "BLOCKED")
            self.assertIn("UNKNOWN", emit.call_args.args[0]["owner_touches_after_launch"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
