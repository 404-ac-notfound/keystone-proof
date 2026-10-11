# Owner gates and fresh-seed launch checklist — 11 Oct 2026

Magic. **Do not launch.** This installation preparation follows Andrew's N1
instruction from frozen candidate `6efb7276e3b45d707458fb59647369c604d5ab98`.
PR #3 stays frozen; freeze-record.md is its historical record. This separate
draft removes the green-KEYSTONE isolation bypass; see installation-n1.md.
This is not merge, activation or launch approval. KEYSTONE #32 remains draft.

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

## Additional owner evidence — about 22:03 MYT / 14:03 UTC

Source: Andrew's typed report in this chat, followed by explicit authorization
for the expiry correction and draft freeze:

> Old OAuth retired: both inference-only Claude Code tokens from 9 Oct revoked on claude.ai (Authorization tokens). New K-14 token (created ~9:41 PM) kept.
> Codex for keystone-proof (chatgpt.com/settings/code-review): Automatic review ON, Review = Follow personal preferences, Trigger = On PR open, Exhaustive review = Follow personal preferences.

Both reports are **OWNER ATTESTED**; no issuer/account probe or token read by
Magic. The timestamps are approximate, not exact credential issuance metadata.

## What is now cleared

| Gate | Evidence basis | Disposition |
|---|---|---|
| Public repository capability | GitHub repo metadata: private=false, visibility=public | VERIFIED; prior private/Free blocker closed |
| Two named environments exist | Public environment GETs, IDs 24011236134 and 24011239056 | VERIFIED |
| Deployment main only | Each policies GET returns exactly one policy, name=main, type=branch | VERIFIED; no wildcard/tag/PR branch admission |
| Unattended environment rules | Each protection_rules contains branch_policy only | VERIFIED current configuration: no required reviewer or wait timer |
| Environment-only fresh credentials | Andrew's original report above | OWNER ATTESTED; no secret metadata/value read |
| Single-repo PAT and actual rights | Andrew's report: Pull requests and Issues read/write, 30 days | OWNER ATTESTED; no test POST or token authentication |
| Old OAuth retirement | Andrew's 21:42 and about 22:03 reports | OWNER ATTESTED GitHub deletion and both old issuer tokens revoked; new K-14 token kept |
| Codex repository review settings | Andrew's about 22:03 report above | OWNER ATTESTED current four settings; no live review claim |
| PAT/pilot expiry mismatch | Controller correction and offline boundary tests | RESOLVED in draft; provider lifetime separated from use-until; ceiling unchanged |
| Admin bypass | Each environment GET: can_admins_bypass=true | OBSERVED limitation; not changed or invented as a new consensus gate |

Raw, non-secret API metadata and verification times are in
[owner-environment-evidence.json](owner-environment-evidence.json). Existence of
branch restrictions does not certify main's own branch protection or secret
values. A repository/organization same-name secret fallback remains forbidden.

## Still needed before launch — concrete order

1. **Complete exact credential metadata and retirement acceptance.** Old-token
   issuer retirement is now recorded as cleared by Andrew. Supply real UTC
   created_at and expires_at for both fresh credentials; no values in receipts.
   Approve each use_until (runtime stop no later than K14_EXPIRES_AT) and Andrew's
   revoke-and-delete responsibility on terminal outcome, cancellation or by
   use_until, whichever comes first. Fresh-token issuance is currently only
   approximate; the runtime template remains unlaunchable until completed.

2. **Expiry correction is prepared and frozen.** A 30-day PAT may have actual
   provider expiry beyond 23 Oct, without extending the pilot. Its positive
   issuance-to-provider-expiry duration must be at most 30 days. Both credentials
   must be valid through their allowed-use deadline, with now < use_until <=
   K14_EXPIRES_AT <= approved_expiry_ceiling <= 2026-10-23T00:00:00Z. This preserves
   the original UTC cutoff (23 Oct 08:00 MYT), rather than extending to that day's
   end. Gates stop at a shorter use_until too. No automatic issuer revocation or
   secret deletion is claimed: Andrew performs and records lifecycle retirement.
   This code correction needs the assigned independent checks below.

3. **Codex target readiness, read-only.** An authorized account seat records
   keystone-proof's repository connection, linked requester access, selected
   managed review route applicability and credit continuation OFF, with time and
   source. The four current repository settings are already OWNER ATTESTED by
   Andrew; they do not establish linked-requester access or bot-draft-PR support. Codex cloud environment existence/ID remains UNKNOWN here. Official
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

5. **Independent final-main rechecks are a hard launch gate.** Urahara and Kobe
   both posted static PASS on frozen 6efb727. This separate N1 revision and any
   installation/merge change need their own evidence. After Andrew-approved
   installation/merge, both recheck the actual final main SHA and supply PASS
   receipts with controller_sha equal to GITHUB_SHA and K14_APPROVED_SHA, real
   same-repo comment URLs and exact body SHA-256s. The read-only gate verifies
   the actual comments' owner publisher, seat, opening-paragraph SHA and PASS.
   The guard also requires main == that SHA. Missing/stale receipts stop before
   launch admission; green KEYSTONE status grants no exception. Runtime template
   slots remain PENDING. Magic does not run their isolation assessment.

6. **Complete the non-secret launch envelope and fresh cash evidence.** Assign
   a new seed issue (>1), unique pilot id and unused claim/attempt slots. Existing
   job/1 and evidence/1 were observed; seed 1 cannot be reused. Fill the preflight
   with source/quote, owner_authorization.controller_author=Magic matching the
   code-pinned author list, exact approved main SHA, real checker comments/body
   hashes, readiness,
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
