# K-14 controller correction and next relay

Status: PREPARED, OFFLINE-TESTED, INACTIVE. No new provider run or review requested.

Andrew authorized diagnosis, correction and a bounded relay on 2026-10-10 in the original KEYSTONE discussion. The existing $0 envelope and account preflight remain applicable. This branch is preparation; it does not satisfy the preflight or amend the live doctrine.

## Diagnosis

Original run: https://github.com/404-ac-notfound/keystone-proof/actions/runs/37908062128

Original PR: https://github.com/404-ac-notfound/keystone-proof/pull/2

Original receipt: https://github.com/404-ac-notfound/keystone-proof/blob/evidence/1/jobs/1/receipt.md

The first look ended NO-VERDICT after 1802 seconds. Fresh reads on 2026-10-10 found zero submitted reviews, zero inline review comments, zero PR reactions and zero check runs on a2835704abaf06a7348ef892ca57a14669996ed3; the only Conversation comment was Actions' receipt link. Poll logs showed no review-fetch error. The earlier checks endpoint 403 is a workflow-token permission defect; the present connector read succeeds and returns an empty list. These observations establish absence of a public PR verdict, not the provider-side cause or absence of invocation.

PR #2 was opened by github-actions[bot]. Repository review enablement, personal preferences, trigger configuration, treatment of this opener, quota and connected-app identity cannot be verified through the current GitHub tools. Official troubleshooting: https://learn.chatgpt.com/docs/third-party/github . Do not infer that the bot opener caused the failure, that adding checks:read will wake Codex, or that a successful old author call proves present credentials/headroom.

## Correction

- Add checks:read so the workflow can inspect diagnostic check runs.
- Publish the receipt first, then fail the receipt job if transport failed or no receipt commit exists. Green execution can no longer hide a recorded transport failure.
- Require verdict artifacts to agree with job outputs, exact expected heads and the pinned verifier, and carry consumed IDs/quoted bound evidence. Reject reused first-look IDs in the second look.
- Reject structured review bindings to another commit even when their body mentions the new SHA.
- Treat bound quota/error/status messages as NO-VERDICT rather than revision findings; retain standard explicit clean and findings output recognition. Unsupported substantive formats fail closed for investigation.
- Run offline controller regression checks before invoking Claude.
- Set SEEDED_ISSUE to UNASSIGNED. The candidate cannot admit a run until a fresh issue is explicitly pinned after preflight. Original job/1 and evidence/1 remain intact.

Validation: 14 stdlib unittest cases, including execution of all six existing parser test functions, passed locally. YAML parsed; embedded shell scripts syntax-checked. No provider invocation, GitHub Actions run, paid API, settings change or merge occurred. These are mechanical tests, not an independent model review or a transport pass.

## Concrete unblock sequence

1. Obtain current owner/account evidence for Codex connection to this private repo, repository Automatic review, personal preferences (including coverage of PRs opened by github-actions[bot]), PR-open trigger and the confirmed verifier login. Read-only access or screenshots suffice; never paste tokens.
2. Record the existing envelope's three $0 cash stops and included headroom, plus whether the previous run's OAuth secret was deleted as required. Current secret availability is UNKNOWN and must be restored only through an authorized owner setup act if needed.
3. Promote the reviewed correction only after readiness; create one fresh issue, pin its number, and emit ready once. No rerun of consumed issue #1, ref deletion or broadened guard.
4. Record the automatic first review and, if findings occur, the bot-requested second review. A clean first review is a partial-path result with revision UNEXERCISED. No owner-authored @codex comment is inserted afterward to disguise recovery as automatic transport.
5. Preserve the frozen receipt, reconcile the test register, and perform the envelope's post-run billing read and secret retirement. Jarvis notification needs its own accessible, configured report listener; the Black Mamba routine is insufficient.

## Final K-23 fixture to stage after transport proof

The held K23-FU-08 fixture requires one author, one independent verifier, one seeded revision, one seeded technical gap and one genuine owner gate. This candidate controller correction is not that completed fixture.

| Key | Fixture / expected observation |
|---|---|
| RELAY-01 | Author consumes an exact kickoff commit; saves the candidate artifact and assumptions. Verifier consumes that exact candidate revision and records a substantive finding. |
| RELAY-02 | Include one disclosed, deliberately seeded defect in the review candidate under a dedicated test branch. It must be independently identified, sent back as a file, corrected by the author, then rechecked at a distinct head. No fabricated verifier post or self-review counts. Define the defect and the verifier's supported review threshold before launch; ordinary automatic review may ignore minor fixture bugs. |
| RELAY-03 | Deliberately omit one required supporting fixture. The seat records its exact missing path under open technical blockers, continues only independent work and never guesses the data. |
| RELAY-04 | End with the real owner decision whether to promote the proven route beyond the test envelope. Publish one bounded ask, wait for Andrew's decision and take no promotion action beforehand. Jarvis forwards the already-authored ask once through a separately verified listener. |
| RELAY-05 | Receipt pins every upstream/downstream head, actual provider/runtime, acknowledgement IDs, assumptions and open technical blockers; records launches separately from Andrew-carried messages. Target: zero routine carried messages after kickoff. |
| RELAY-06 | Final delivery contains brief evidence-backed bullets. Exact-chat continuity is separately scored; fresh Git-backed invocations earn no existing-thread claim. |

Ready report for Jarvis after his listener is configured:

Sir, the KEYSTONE handoff test results are in:
- Claude author leg: passed in the 9 October pilot.
- Codex return leg: failed acceptance; no qualifying verdict reached GitHub.
- Controller correction: prepared; offline checks passed.
- Full relay: blocked before a new run on account-side review readiness and $0 preflight evidence.

No delivery of that report to Jarvis is claimed.
