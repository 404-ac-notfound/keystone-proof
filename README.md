# keystone-proof

Private proof repo for the KEYSTONE K-14 transport pilot (one bounded run).

- Design and terms: `cabinet/thread-handoffs/2026-10-07/K14-PILOT-ENVELOPE-PROPOSAL-V3.md` in the KEYSTONE repo (approved by Andrew 2026-10-09, as amended 6).
- Workflow: `.github/workflows/k14-pilot.yml`. Trigger: the `ready` label on issue #1.
- Spend: $0. Expiry: 2026-10-23. Off switch: disable the workflow, delete the `CLAUDE_CODE_OAUTH_TOKEN` secret.
- Nothing here is production code. `calc.py` is a seeded bug for the author seat to fix.
