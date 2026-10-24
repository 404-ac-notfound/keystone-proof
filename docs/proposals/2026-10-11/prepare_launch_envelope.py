#!/usr/bin/env python3
"""Prepare non-secret Actions variable values offline; never set variables or launch."""
import argparse
import json
from pathlib import Path

from k14_controller import gates, require, utc, validate_config_shape, now_utc, launch_budget, PREFLIGHT_DEADLINE, ADMISSION_PILOT


def build(preflight, main_sha, expires_at, cash_checked_at, included_minutes,
          cash_stop_verified, now=None):
    validate_config_shape(preflight)
    if preflight.get("configuration_admission") is not None or preflight.get("pilot_id") == ADMISSION_PILOT:
        now = now or now_utc()
        require(now < utc(PREFLIGHT_DEADLINE), "16:00 MYT preflight deadline reached; stand down")
        preflight = {**preflight, "preflight_completed_at": now.isoformat().replace("+00:00", "Z")}
    require(cash_stop_verified is True, "fresh cash-stop verification required")
    require(type(included_minutes) is int, "included minutes must be an integer")
    author = preflight.get("author_credential", {})
    bound = author.get("revocation_bound", {})
    if bound:
        require(utc(expires_at) <= utc(bound.get("revoke_by")),
                "launch envelope exceeds owner OAuth revocation bound")
    encoded = json.dumps(preflight, separators=(",", ":"), ensure_ascii=True)
    require(len(encoded.encode()) < 48000, "preflight exceeds Actions variable size")
    variables = {
        "K14_ENABLED": "true",
        "K14_APPROVED_SHA": main_sha,
        "K14_EXPIRES_AT": expires_at,
        "K14_PREFLIGHT_JSON": encoded,
        "K14_CASH_CHECKED_AT": cash_checked_at,
        "K14_CASH_STOP_VERIFIED": "true",
        "K14_INCLUDED_MINUTES": str(included_minutes),
    }
    gates(preflight, {**variables, "GH_REPO": preflight.get("repository"),
                     "GITHUB_RUN_ATTEMPT": "1", "GITHUB_SHA": main_sha}, now)
    launch_budget(preflight, variables, now)
    return variables


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--preflight", type=Path, required=True)
    p.add_argument("--main-sha", required=True)
    p.add_argument("--expires-at", required=True)
    p.add_argument("--cash-checked-at", required=True)
    p.add_argument("--included-minutes", type=int, required=True)
    p.add_argument("--cash-stop-verified", action="store_true")
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    values = build(json.loads(a.preflight.read_text()), a.main_sha, a.expires_at,
                   a.cash_checked_at, a.included_minutes, a.cash_stop_verified)
    a.output.write_text(json.dumps(values, indent=2) + "\n")
    print("Prepared seven variable values offline. Nothing was set or launched.")


if __name__ == "__main__":
    main()

