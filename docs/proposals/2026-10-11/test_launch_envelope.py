"""Offline envelope contract tests; synthetic evidence only."""
import json
import unittest
from test_managed_controller import fixture, A, B, NOW, STAMP, EXPIRES
from prepare_launch_envelope import build
from k14_controller import Stop


class Envelope(unittest.TestCase):
    def test_exact_seven_strings_match_workflow_and_preserve_preflight(self):
        c, _ = fixture()
        v = build(c, A, EXPIRES, STAMP, 125, True, NOW)
        self.assertEqual(set(v), {"K14_ENABLED", "K14_APPROVED_SHA", "K14_EXPIRES_AT",
            "K14_PREFLIGHT_JSON", "K14_CASH_CHECKED_AT", "K14_CASH_STOP_VERIFIED", "K14_INCLUDED_MINUTES"})
        self.assertTrue(all(isinstance(x, str) for x in v.values()))
        self.assertEqual(json.loads(v["K14_PREFLIGHT_JSON"]), c)

    def test_stale_sha_cash_or_unverified_stop_cannot_produce_envelope(self):
        c, _ = fixture()
        for sha, stamp, minutes, verified in ((B, STAMP, 125, True),
                (A, "2026-10-10T00:00:00Z", 125, True),
                (A, STAMP, 124, True), (A, STAMP, 125, False)):
            with self.subTest(sha=sha, stamp=stamp, minutes=minutes), self.assertRaises(Stop):
                build(c, sha, EXPIRES, stamp, minutes, verified, NOW)

    def test_oauth_bound_limits_entire_launch_window(self):
        c, _ = fixture()
        c['author_credential'].update(expires_at=None, use_until='2026-10-11T02:15:00Z',
            revocation_bound={'basis':'OWNER_REVOCATION_BOUND', 'owner':c['launch_login'],
                'revoke_by':'2026-10-11T02:15:00Z', 'evidence':'synthetic'})
        with self.assertRaisesRegex(Stop, 'revocation bound'):
            build(c, A, EXPIRES, STAMP, 125, True, NOW)
