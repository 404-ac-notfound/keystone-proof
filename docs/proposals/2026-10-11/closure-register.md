# Review repair closure register

> Current reconciliation: [12 Oct handoff](reconciliation-20261012.md). PR #3 e3bbab1 and PR #4 d712b74 are joined in one inactive draft; the author allowlist and strict comment verification are retained. OAuth unknown expiry uses its separate owner revocation bound. See launch-envelope-20261012.md and final-acceptance-alignment-20261012.md for current scope and gaps. Earlier SHA/check counts below are historical.

Baseline: [KEYSTONE #33 final AGREED closure](https://github.com/404-ac-notfound/KEYSTONE/issues/33#issuecomment-6103037544).
Author: Magic. Scope: inactive drafts only. No live proof or isolation PASS.

| Requirement | Status | Implementation / evidence | Follow-up / next owner |
|---|---|---|---|
| Item 3: real same-run invocation | IMPLEMENTED | k14-managed.yml.disabled and k14_controller.py: distinct request/poll jobs, no workflow-event hop | Live bot-PR support unproven; Andrew launch gate |
| Item 4: global two reviews, one revision, diff limits | VERIFIED, offline only | Synthetic tests; create-only refs and bounds before requests | Live provider/run evidence needed |
| Items 3/6: credentials and API OFF | IMPLEMENTED / OWNER PROVISIONED | Read-only author/poll; independent publisher; PAT only request POST; fresh OAuth plan; API jobs hard OFF | Exact expiry/lifecycle and selected-route readiness still needed; provisioning OWNER ATTESTED |
| Item 3: environment/access readiness | BLOCKED | environment-status.md; template UNKNOWN; actual KEYSTONE connector reply linked | Authorized read-only readiness record; Andrew account decisions |
| Item 6: old OAuth retirement | CLEARED, OWNER ATTESTED | Andrew 21:42 MYT GitHub deletion; about 22:03 MYT both old issuer tokens revoked, new K-14 kept | Record new-token metadata and owner retirement acceptance |
| Item 7: independent isolation evidence | CANDIDATE PASS; FINAL MAIN PENDING | Both seats' static PASS at frozen 6efb727; runtime slots remain PENDING | **Urahara and Kobe** recheck this change and final installed main SHA; Magic does not assess isolation |
| Item 7 / N1: proof/canary/adoption order | HARD ISOLATION GATE, draft only | Green-KEYSTONE alternative removed; both assigned PASS receipts must bind to final launch SHA | Andrew gates; green KEYSTONE retained only for later #32 adoption/migration |
| Exact-head review/tests/final usage/owner-touch/retirement receipt | PARTIAL | Poll/final-check/receipt implementation; no live verdict, billing or retirement proof | Independent post-run audit; unknowns never self-issue PASS |

Lesson migration and vendor cleanup belong to #32's later gated draft work.
This register records this controller revision, not a new shop constitution.

## 11 Oct review fix-ups

Urahara's static PASS and Kobe's FAIL at 5f25488 are historical. Andrew permits
external full-SHA actions and downgraded Kobe's FAIL to fix-ups. Both new-revision
checker slots remain PENDING; Magic has not performed their check.

Runtime-and-environment-fixups.md maps the bootstrap/image/pytest/legacy-workflow
changes, exact sources and limitations. Fresh OAuth/PAT jobs now reference
protected environments; the earlier Free/private capability blocker was superseded by Andrew's public
repo decision at 21:42 MYT. Public visibility and main-only environment rules
are now API verified. Secret placement/deletion is OWNER ATTESTED. Magic made
no account changes. Remaining Codex route/lifecycle and final independent checks
are in owner-gates-20261011.md. The expiry mismatch is now corrected in draft.

## Owner gate update — 21:42 MYT

Public capability RESOLVED; two credential environments exist, main-only policy
verified through public GETs. Admin bypass remains enabled. Provisioning and
old GitHub-secret removal are OWNER ATTESTED. The subsequent about 22:03 MYT
report confirms both old issuer tokens revoked, new K-14 kept, and current
repository review settings. Exact new-token UTC metadata/lifecycle acceptance
remain pending. The controller now separates provider expiry from allowed use,
measures PAT lifetime from issuance and enforces the unchanged 23 Oct UTC ceiling.
See freeze-record.md; no activation or launch is granted.

## Installation preparation — N1

Andrew's instruction after Kobe's 6efb727 PASS removes the fallback in the next
revision. Both final-main checker receipts are mandatory. Candidate PASS comments
are historical evidence, not permission to fill this new revision's runtime slots.
The separate installation draft leaves frozen PR #3 and main unchanged; all
managed/API workflow candidates remain inactive. See installation-n1.md.

## Urahara QA: F3/F4 follow-up

Urahara passed static isolation/four checks at 0df1a61; that evidence does not
certify this new revision. F4 is addressed by the code-pinned `{Magic}` author
list and matching owner authorization. F3's text-only receipt gap is hardened
with canonical same-repo comment URLs, pinned body SHA-256 and read-only checks
of the real comment's ID/parent/owner publisher/raw-body digest and exact
`Seat: PASS <full approved SHA>` first line before admission and non-receipt controller stages. Human reviewer provenance remains
Andrew's trust boundary. Template slots stay PENDING with null evidence/hashes.
PyYAML is hash-locked for offline QA only; production locks and workflows are
unchanged. 48 controller + 7 runtime tests passed in the clean QA venv. Both
assigned seats recheck the changed revision and final installed main.


## Kobe FAIL: strict review-comment protocol

[Kobe's FAIL at 205fb9c](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6110786143)
found ambiguous verdict and stale-SHA acceptance, a CRLF paragraph escape, and
malformed API records raising AttributeError. The draft replaces permissive
paragraph/Isolation-label matching with one exact seat/PASS/approved-SHA first
line. Raw UTF-8 hashes remain exact; CRLF is normalized only for parsing, other
full SHAs in the opening paragraph stop, and malformed records raise Stop.
The 48 controller + 7 runtime tests are synthetic author validation, not a new
checker verdict. Both assigned seats review this SHA and later final main;
Andrew's installation, credential, cash and launch gates remain unchanged.
