# Owner gates and fresh-seed launch checklist — 11 Oct 2026

Magic. **Do not launch.** This is a records-only revision of draft PR #3 from
parent `5ebba9a865acfb8f3502a33487c1beff434c67a6`. Controller/runtime/workflow
implementations are unchanged. This record is not merge, activation or launch
approval. KEYSTONE #32 remains draft.

## Andrew's authenticated owner report

Source: Andrew's typed message in the Magic chat, 11 Oct 2026, **21:42 MYT /
13:42 UTC**, received at 21:43 MYT. Scope: capability/environment records,
read-only protection verification, Codex status and remaining gates. Original:

> keystone-proof is now PUBLIC (Urahara pre-publication scan: no secrets; Andrew accepted his email on 5 old commits; email privacy now ON).
> Environments k14-author-owner-approved and k14-review-owner-approved created, deployment limited to the main branch only.
> K14_AUTHOR_OAUTH_TOKEN (fresh claude setup-token) is in the author env; K14_REVIEW_REQUEST_TOKEN (fine-grained PAT, keystone-proof only, PR and Issues read and write, 30 days) is in the review env. No repo-level copies; old CLAUDE_CODE_OAUTH_TOKEN deleted.

The scan, accepted historical email exposure and email-privacy change are owner
reported; Magic did not rerun the publication scan or inspect account email
settings. No historical email address is copied into this receipt.

## What is now cleared

| Gate | Evidence basis | Disposition |
|---|---|---|
| Public repository capability | GitHub repo metadata: private=false, visibility=public | VERIFIED; prior private/Free blocker closed |
| Two named environments exist | Public environment GETs, IDs 24011236134 and 24011239056 | VERIFIED |
| Deployment main only | Each policies GET returns exactly one policy, name=main, type=branch | VERIFIED; no wildcard/tag/PR branch admission |
| Unattended environment rules | Each protection_rules contains branch_policy only | VERIFIED current configuration: no required reviewer or wait timer |
| Environment-only fresh credentials | Andrew's original report above | OWNER ATTESTED; no secret metadata/value read |
| Single-repo PAT and actual rights | Andrew's report: Pull requests and Issues read/write, 30 days | OWNER ATTESTED; no test POST or token authentication |
| Old GitHub secret removal | Andrew's report | OWNER ATTESTED deletion; issuer revocation still UNKNOWN |
| Admin bypass | Each environment GET: can_admins_bypass=true | OBSERVED limitation; not changed or invented as a new consensus gate |

Raw, non-secret API metadata and verification times are in
[owner-environment-evidence.json](owner-environment-evidence.json). Existence of
branch restrictions does not certify main's own branch protection or secret
values. A repository/organization same-name secret fallback remains forbidden.

## Still needed before launch — concrete order

1. **Finish issuer retirement and expiry evidence.** Record revocation of the
   old issued OAuth, not just its GitHub-secret deletion. If issuer revocation
   invalidates the fresh token too, Andrew controls replacement after revocation.
   Supply exact UTC expiry for both fresh credentials and the terminal/cancel/
   expiry revoke-and-delete owner. Token values must never enter the receipt.

2. **Resolve the draft's credential-expiry mismatch.** Current k14_controller.py
   gates require each credential expires_at to be no later than K14_EXPIRES_AT,
   and the request credential no later than 30 days from invocation. The
   provisioned 30-day PAT runs beyond the old 23 October pilot envelope; the
   fresh setup-token's expiry is not reported. Do not enter an invented short
   expires_at just to pass. A reviewed draft correction can separate provider
   expiry from the allowed-use/revocation deadline while preserving the pilot's
   runtime stop and 30-day PAT ceiling. Alternatively Andrew supplies credentials
   whose actual expiries fit the approved pilot window. No code/lifetime/secret
   change is made by this records revision; an extended pilot window is not
   authorized by the setup message.

3. **Codex target readiness, read-only.** An authorized account seat records
   keystone-proof's repository connection, linked requester access, selected
   managed review path/configuration and credit continuation OFF, with time and
   source. Codex cloud environment existence/ID remains UNKNOWN here. Official
   automatic cloud reviews do not require a newly managed cloud environment;
   record applicability for the actual route rather than creating one by default.
   Bot-authored draft-PR coverage is the experiment's outcome, not a claim to
   prove by launching a separate test now. No reliance on the All PRs toggle.

4. **Prepare and approve the actual activation revision.** PR #3 is still draft.
   The managed controller is a .disabled proposal outside .github/workflows;
   main remains 453e20497c019562a660dd260c6eff098b8ea2a2. API workflow inventory
   still lists the legacy k14-pilot as active; its retirement stub exists only on
   the draft branch. Installation/retirement/merge requires Andrew's explicit
   approval; missing/OFF K14_ENABLED must remain in effect until launch approval.
   Environment main-only rules mean the credential jobs cannot be tested on a
   draft/PR branch. No need to broaden those environment rules.

5. **Independent checks on the final launch revision.** Urahara and Kobe must
   assess the completed fixes; their comments fetched now still concern 5f25488.
   This records commit creates no isolation PASS. Freeze the intended code and
   activation diff before their check; bind or recheck the actual final main SHA
   after any merge/installation change, because the guard requires
   main == GITHUB_SHA == K14_APPROVED_SHA. Magic does not run their isolation
   assessment. Missing evidence follows the agreed green-main prerequisite.

6. **Complete the non-secret launch envelope and fresh cash evidence.** Assign
   a new seed issue (>1), unique pilot id and unused claim/attempt slots. Existing
   job/1 and evidence/1 were observed; seed 1 cannot be reused. Fill the preflight
   with source/quote, exact approved main SHA, checker evidence, readiness,
   credential lifecycle and UTC expiry ceiling. Set the owner-approved
   K14_APPROVED_SHA, K14_PREFLIGHT_JSON and K14_EXPIRES_AT only under the applicable
   owner authorization. Record cash stops, current included provider headroom and
   paid continuation OFF; K14_CASH_CHECKED_AT must be at most two hours old at
   every gated step and K14_INCLUDED_MINUTES >=125. Public visibility does not
   populate these runtime values. Keep the global two-review/one-revision and
   50-file/1,000-line/128-KiB caps.

7. **Accept the exact hosted image policy and final launch tap.** The locked
   image admission remains ubuntu24 / 20261004.327.1, system Python 3.12.3,
   x86_64. GitHub must supply that image or every job stops before checkout.
   Scheduling availability was not verified by starting a job. A changed-image
   re-pin needs its own reviewed revision/Andrew gate, not a silent fallback.
   Once items above are cleared, Andrew approves the exact fresh-seed run,
   enablement and ready-label tap. No issue was created/labeled and no variable
   changed now.

The launch receipt must quote the applicable authenticated approval. Setup
approval does not authorize launch. Keep runtime trace/files/refs, exact review
head/read-back, verdict/check evidence, timing/usage, zero owner transport touches
and post-run credential retirement in the receipt. Final billing/retirement
unknowns remain BLOCKED until independent evidence resolves them.
