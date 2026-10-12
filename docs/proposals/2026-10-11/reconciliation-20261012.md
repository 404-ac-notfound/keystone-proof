# K-14 convergence memo — draft, 12 October 2026

**Authority:** Andrew's request to reconcile keystone-proof PR #3 and PR #4, propose merge order, align against the owner-approved KEYSTONE continuity final acceptance specification, and push **draft only**. No installation/merge/activation/launch authorization.

## Provenance and source refs

- PR #3 at `e3bbab1697f374cb58528d3d908ca9350ad02b20`: independent Urahara isolation PASS; owner OAuth revoke-by, offline seven-variable envelope and K-23 gap register. [Urahara review](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6111840330).
- PR #4 at `d712b7451ac90d55bfa02516dfd25de26783252c`: code-pinned Magic author list (F1/F4); canonical Urahara/Kobe first-line PASS for full exact SHA; same-repo comment identity/publisher/raw SHA-256 verification (F3/F5); reject ambiguous and malformed comments. [Kobe](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6110975595) and [Urahara](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6111005767) PASSes are draft-only.
- Merge base: `6efb7276e3b45d707458fb59647369c604d5ab98`. The branches diverge: PR #4 lacks PR #3's owner-bound / envelope / acceptance work, while PR #3 lacks PR #4's strict record and author gates.
- Canonical external spec: [KEYSTONE final acceptance R1, pinned commit 39e25bb](https://github.com/404-ac-notfound/KEYSTONE/blob/39e25bb6846a44ea56856d4f1b8af129401ac5f5/cabinet/specs/KEYSTONE-CONTINUITY-SYSTEM-FINAL-ACCEPTANCE-SPEC-R1.md), owner-approved 8 Oct. Referenced for design comparison only, never fetched at K-14 runtime.

## One reconciliation line

This draft uses #4 as the security-gate base and explicitly incorporates the additional #3 changes:

1. Retain #4 F1/F4 author allowlist `{Magic}`, owner-author matching and both final-main SHA-bound Urahara/Kobe receipts. Retain F3/F5 read-only comment GET verification, exact first-line `Seat: PASS <sha>`, exact raw UTF-8 hash, CRLF-for-parse-only and malformed API fail-close.
2. Restore #3's **author OAuth only** allowance for *unknown provider expiry* under `OWNER_REVOCATION_BOUND`. The owner-committed `revoke_by` is conservatively `2026-10-22T00:00:00Z` (22 Oct 08:00 MYT). `now < use_until <= min(K14_EXPIRES_AT, revoke_by)` remains mandatory. This gate does **not** revoke the issuer token. The review-request PAT has no such exception: record real creation, provider expiry and 0 < provider lifetime <= 30 days.
3. Retain #4 null/PENDING comment URL/body-hash slots and #3 null/PENDING launch fields. The imported envelope generator remains offline and cannot set variables or activate the kill switch.
4. Port #3's final acceptance mapping and receipt scope: `K14_TRANSPORT_SUBTEST`, `final_continuity_acceptance.outcome=BLOCKED`, `build_complete=false`. No calculator transport outcome may promote K-23.
5. Extra fail-closed hardening proposed here: malformed/non-object isolation receipt entries raise `Stop` rather than `AttributeError` (N2); only the canonical headline may occupy the opening paragraph, so contradictory line-2 text is rejected (N1). Retain later *separate paragraphs* for historical reviews/launch blockers; Andrew must review whole comments before pinning.

## Proposed Andrew merge order (no merges performed)

**Preferred: one combined PR, one owner-approved installation merge.**

1. Review this new combined draft, compared against both pinned heads. **Hold** #3 and #4; do not merge either independently. New commits invalidate their previous candidate PASSes.
2. Request fresh independent Kobe and Urahara reviews on the **combined draft head SHA** (including the new N1/N2 behavior and author-owner-bound exception); resolve any findings on that same line. Do not self-issue independent PASS.
3. After Andrew explicitly authorizes installation, merge **only** this reconciled PR to keystone-proof main. Historical #3/#4 may then be closed as superseded **without merging**; do not silently close them during this draft stage.
4. Both seats independently recheck the **actual installed main commit SHA**. Collect exact GitHub comment URL, body SHA-256 and canonical first line for both and have Andrew check full bodies/provenance before owner-pinning. Reconcile any installation change at another SHA and recheck again.
5. Separately finish fresh seed, route/readiness, expiry/retirement, cash, variables, final-main evidence and explicit Andrew enablement/launch gate. `K14_ENABLED` stays false/missing until the *separate* launch yes. Do not set real variables/secrets here.
6. Sequence after genuine K-14 evidence remains: independently audited K-14 transport PASS → approved second-repo canary → green KEYSTONE/#32 adoption/migration → vendor cleanup. K-23 final image continuity acceptance remains its own end-to-end test.

**Rejected sequence:** merge #3 and #4 independently or use stale #3/#4 candidate checks as installed-main certification. A cherry-picked SHA or merge commit is a new SHA requiring fresh evidence.

## Two distinct PASS contracts

### K-14 scoped transport subtest — only after a real run

One authorized fresh-seed run at the installed pinned head; both verified independent final-main receipts; owner/cash/credential and $0/125-minute limits; correct author publish/linked-user managed review, no more than two requests and one author revision; exact-head review verdict and final calculator tests; recorded API/ref/job IDs and observed owner touches/usage; independent post-run audit. Unknown usage, billing or retirement evidence remains BLOCKED. This proves *transport*, not final continuity.

### K-23 owner-approved FINAL acceptance — real creative-image run

The full play is `Andrew creative request → Git PG plan → Kobe independent PASS on current plan → Urahara method PASS → Shaq image generation/seat QC and Git completion receipt → exactly one finished image surfaced to Andrew`. Required-change loops must self-relay; a material plan revision after Kobe PASS returns through Kobe/Urahara. Every seat logs input pointer, ack, task/session pointer, resume_mode, waiting_for, resume event, output pointer, verdict, assumptions, blockers, next seat and timestamp. Initial wake and ongoing resume are separate evidence.

| Metric | R1 PASS target | Status in K-14 calculator |
|---|---:|---|
| Andrew launches | 1 | Not observed for final fixture |
| Andrew-carried messages after launch | 0 | Not demonstrated end to end |
| Andrew manual seat wake/resume | 0 | Not demonstrated end to end |
| Intermediate Andrew approvals | 0 | Not demonstrated end to end |
| Kobe current-plan verification closure | 1 | Missing (isolation ≠ plan verification) |
| Urahara current-plan method closure | 1 | Missing (isolation ≠ method gate) |
| Shaq execution/QC completion | 1 | Missing specialist/image path |
| Final user-visible deliverable | 1 image | Missing image generation and final delivery |
| Intermediate user-visible status | 0 | Missing display/notification suppression evidence |

**No K-23 PASS or build_complete until every metric is observed in a real run.** A K-14 calculator PASS cannot complete KEYSTONE; no automatic W-grade promotion.

## Validation and unproven claims

This draft carries new test cases for owner-only OAuth bound, strict comment-record gates, malformed receipt shapes, contradictory headline paragraphs, envelope generation and always-BLOCKED K-23 receipt. They are **synthetic/offline tests, not live execution proof**. Existing #4 candidate QA (55 passing tests; synthetic) does not certify this new SHA. The new combined suite must be executed with the pinned QA environment by a reviewer; no model or provider call is authorized as part of this draft.

Open: main-install approval, fresh combined-head Kobe/Urahara checks, both installed-main checks, real PAT dates and author issuance, owner retirement acceptance, current linked-user/managed review access and paid credits OFF, cash evidence, seven runtime variables, fresh seed/pilot and launch authorization. Runner image `20261004.327.1` may drift: pin mismatch stops, never silently relax the runner guard. F2: moved main may burn the create-only pilot claim; use a new pilot id, never reuse/delete the old claim.
