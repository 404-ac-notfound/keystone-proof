"""Offline synthetic expiry evidence only; never a credential or launch envelope."""
import unittest
from unittest.mock import patch

from test_managed_controller import fixture, m, A
from prepare_launch_envelope import build
from k14_controller import Stop as EnvelopeStop

NOW = m.utc("2026-10-14T00:00:00Z")
CEILING = "2026-10-22T00:00:00Z"


def date_fixture(date="2026-11-09"):
    c, e = fixture()
    c["approved_expiry_ceiling"] = e["K14_EXPIRES_AT"] = CEILING
    e["K14_CASH_CHECKED_AT"] = "2026-10-14T00:00:00Z"
    c["author_credential"].update(expires_at=CEILING, use_until=CEILING)
    c["request_credential"].update(
        created_at="2026-10-11T13:35:58Z", use_until=CEILING,
        expires_at=None, expiry_precision="DATE", provider_expiry_date=date,
        provider_expiry_evidence="SYNTHETIC provider date source",
        display_timezone=None, validity_bound_basis="DATE_EARLIEST_INSTANT")
    return c, e


class ExpiryPrecision(unittest.TestCase):
    def test_current_date_evidence_still_stops_before_any_api(self):
        c, e = date_fixture("2026-11-10")
        with patch.dict(m.os.environ, e), patch.object(m, "now_utc", return_value=NOW), \
                patch.object(m, "api") as api:
            with self.assertRaisesRegex(m.Stop, "exceeds 30 days"):
                m.guard(c)
            api.assert_not_called()

    def test_shorter_date_admits_only_synthetic_complete_envelope(self):
        c, e = date_fixture()
        self.assertEqual(m.gates(c, e, NOW), A)
        self.assertEqual(build(c, A, CEILING, e["K14_CASH_CHECKED_AT"], 125, True, NOW)
                         ["K14_EXPIRES_AT"], CEILING)

    def test_bounds_use_opposite_extremes_without_expiry_invention(self):
        c, _ = date_fixture("2026-11-10")
        self.assertEqual(m.request_expiry_bounds(c["request_credential"]),
                         (m.utc("2026-11-09T10:00:00Z"), m.utc("2026-11-11T12:00:00Z")))
        self.assertIsNone(c["request_credential"]["expires_at"])

    def test_use_until_cannot_exceed_earliest_possible_expiry(self):
        c, e = date_fixture("2026-10-21")
        c["request_credential"]["use_until"] = "2026-10-20T10:00:00Z"
        self.assertEqual(m.gates(c, e, NOW), A)
        c["request_credential"]["use_until"] = "2026-10-20T10:00:01Z"
        with self.assertRaisesRegex(m.Stop, "outside allowed-use"):
            m.gates(c, e, NOW)

    def test_lifetime_upper_bound_inclusive_at_30_days(self):
        c, e = date_fixture()
        c["request_credential"]["created_at"] = "2026-10-11T12:00:00Z"
        self.assertEqual(m.gates(c, e, NOW), A)
        c["request_credential"]["created_at"] = "2026-10-11T11:59:59Z"
        with self.assertRaisesRegex(m.Stop, "exceeds 30 days"):
            m.gates(c, e, NOW)

    def test_invalid_dates_and_ambiguous_schema_stop(self):
        values = [None, "", 20261109, "2026/11/09", "2026-11-09Z", "2026-11-09T00:00",
                  "2026-11-09+08:00", "2026-2-03", "2026-02-29", "2026-13-01",
                  "0001-01-01", "9999-12-31"]
        for value in values:
            c, e = date_fixture(value)
            with self.subTest(value=value), self.assertRaises(m.Stop):
                m.gates(c, e, NOW)
        for key, value in [("expiry_precision", "UNKNOWN"), ("expiry_precision", None),
                           ("expiry_precision", "EXACT"), ("expires_at", CEILING),
                           ("provider_expiry_evidence", " "), ("validity_bound_basis", "EXACT"),
                           ("display_timezone", "+08:00")]:
            c, e = date_fixture()
            c["request_credential"][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(m.Stop):
                m.gates(c, e, NOW)

    def test_exact_path_preserved_and_date_conflict_stops(self):
        c, e = fixture()
        from test_managed_controller import NOW as old_now
        self.assertEqual(m.gates(c, e, old_now), A)
        c["request_credential"]["expiry_precision"] = "EXACT"
        self.assertEqual(m.gates(c, e, old_now), A)
        c["request_credential"]["provider_expiry_date"] = "2026-10-11"
        with self.assertRaises(m.Stop):
            m.gates(c, e, old_now)

    def test_22_oct_ceiling_is_not_overridable(self):
        c, e = date_fixture()
        c["approved_expiry_ceiling"] = e["K14_EXPIRES_AT"] = "2026-10-22T00:00:01Z"
        with self.assertRaises(m.Stop):
            m.gates(c, e, NOW)
        c, e = date_fixture()
        c["author_credential"].update(expires_at=None, revocation_bound={
            "basis": "OWNER_REVOCATION_BOUND", "owner": "404-ac-notfound", "evidence": "synthetic",
            "revoke_by": "2026-10-22T00:00:01Z"})
        with self.assertRaises(m.Stop):
            m.gates(c, e, NOW)
        for kind in ("author_credential", "request_credential"):
            c, e = date_fixture()
            c[kind]["use_until"] = "2026-10-22T00:00:01Z"
            with self.subTest(kind=kind), self.assertRaises(m.Stop):
                m.gates(c, e, NOW)

    def test_non_z_credential_and_envelope_timestamps_stop(self):
        for value in ("2026-10-22", "2026-10-22T00:00:00", "2026-10-22T00:00:00+00:00"):
            for kind in ("author_credential", "request_credential"):
                c, e = date_fixture()
                c[kind]["use_until"] = value
                with self.subTest(kind=kind, value=value), self.assertRaises(m.Stop):
                    m.gates(c, e, NOW)
            c, e = date_fixture()
            with self.assertRaises(EnvelopeStop):
                build(c, A, value, e["K14_CASH_CHECKED_AT"], 125, True, NOW)

    def test_leap_day_and_month_boundaries(self):
        c, _ = date_fixture("2028-02-29")
        self.assertEqual(m.request_expiry_bounds(c["request_credential"]),
                         (m.utc("2028-02-28T10:00:00Z"), m.utc("2028-03-01T12:00:00Z")))
        c, _ = date_fixture("2026-12-31")
        self.assertEqual(m.request_expiry_bounds(c["request_credential"]),
                         (m.utc("2026-12-30T10:00:00Z"), m.utc("2027-01-01T12:00:00Z")))

