# K-14 installation draft — reviewed controller, launch OFF

Magic. Prepared 12 October 2026 MYT. This is a new draft branch based on
`d712b7451ac90d55bfa02516dfd25de26783252c`; PR #4 remains frozen at that SHA.
No merge, secret/environment/variable update, label, model call or launch has
been performed. GitHub default main was read at
`453e20497c019562a660dd260c6eff098b8ea2a2` during preparation.

## Exact proposed installation

- Add `.github/workflows/k14-managed.yml`, derived from the reviewed
  `docs/proposals/2026-10-11/k14-managed.yml.disabled` without changing any job
  steps, permissions, runner guard, external action SHA, secret reference,
  environment, timeout, artifact, job dependency or controller/runtime path.
- The new file changes the proposal header/name and adds a job-level condition
  to guard and receipt: repository keystone-proof, default main ref, owner sender
  404-ac-notfound, label ready, and `vars.K14_ENABLED == 'true'`. Receipt keeps
  `always()` but uses the same condition. OFF, missing or any non-literal-true
  switch skips every job, including receipt, without allocating a runner.
- The inherited `.github/workflows/k14-pilot.yml` is the reviewed retirement
  stub: permissions empty, its only job hard `if: false`, no uses or secrets.
  Merging this complete installation PR would replace main's old seed-1 pilot
  with that stub. No separate merge of PR #3 or #4 is required or authorized.
- The API workflow alternative and original managed proposal stay `.disabled`.
  Native Claude runtime, controller, config, production/QA locks and tests remain
  byte-identical to d712b74. The runnable file continues to use the reviewed
  scripts under docs/proposals/2026-10-11; no unreviewed relocation is introduced.

Publishing the branch or draft PR does not install the workflow on default main.
Its only event is issues/labeled, with no push, pull_request, schedule or dispatch
trigger. The old pilot on main remains live until approved retirement/merge;
leave its seed-1 ready label untouched. Installation is still an owner decision.

## Review evidence and accepted limits

Magic read both complete current draft comments and confirmed the PR #4 head:

- [Kobe PASS](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6110975595):
  canonical first line at d712b74; all six parser fixes verified, 55 tests passed;
  109 probes included two malformed owner-receipt findings (N2), with separate
  informational probes confirming N1. No parser verdict/stale-SHA attacks admitted.
- [Urahara PASS](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6111005767):
  canonical first line at the same SHA; independent isolation PASS, 55 tests and
  25 probes behaved as expected; reconciled with Kobe after his own checks.

Neither comment retracts its draft PASS or reports a blocking contradiction.
Both explicitly exclude final installed main and live provider/runner/cash proof.
They are historical draft evidence, not launch receipts for another SHA. Magic
has not run or certified the assigned independent isolation checks.

Retained non-blockers: headline PASS can be contradicted below it (N1); malformed
owner-supplied receipt entries fail closed with a traceback instead of BLOCKED
(N2); comment scope/provenance is owner-trusted (N3). Before pinning final-main
receipts, Magic can fetch/read the entire comments, flag contradictions, verify
that scope is final-main isolation and prepare exact raw-body hashes for Andrew's
approval. Andrew owns reviewer provenance/acceptance; manual line-by-line auditing
is not an extra mandatory owner task. Put final-main scope after a blank line.
F2 remains: moved main consumes the unique claim; never delete/reuse that pilot id.

## One installation decision, then a separate launch decision

1. Urahara and Kobe review the installation delta independently. Previous draft
   PASS does not automatically certify a new commit. No author-run isolation check.
2. Andrew approves this exact installation head and retirement of the obsolete
   workflow. Before merge, an authorized account seat confirms `K14_ENABLED` is
   missing/OFF; do not print preflight JSON or secret values into PR comments.
   Merge approval is not inferred from discussion or from this draft publication.
3. After the approved merge, read actual default-main SHA. Both seats recheck that
   final installed tree and post fresh comments. First line exactly
   `<Seat>: PASS <full final-main SHA>` (Kobe/Urahara); after a blank line state
   final-main isolation scope, findings and limits. These two receipts must bind
   `controller_sha == GITHUB_SHA == K14_APPROVED_SHA`. Do not reuse draft receipts.
4. Prepare the owner envelope and collect the remaining evidence below. Keep
   K14_ENABLED OFF while checks and variable/config preparation are incomplete.
5. Andrew gives separate launch approval bound to that final SHA, new seed and
   pilot id, allowed-use window and fixed cash/review limits. Only then may an
   authorized seat enable the switch and apply ready once to the fresh seed.
   No launch approval is sought or claimed by publishing this PR.

## Remaining owner/account evidence — no token values

| Gate | Existing evidence | Still required before launch |
| --- | --- | --- |
| Author credential | Fresh K-14 token in author environment, owner attested; both old 9-Oct tokens revoked and old repo secret deleted | Exact UTC created_at/expires_at; approved use_until; terminal/cancel/deadline revoke-and-delete acceptance |
| Review-request PAT | Fine-grained keystone-proof-only, PR/Issues read-write, 30 days, review environment only | Exact UTC created_at/expires_at; positive lifetime <=30 days; approved use_until and lifecycle acceptance |
| Allowed-use window | Original ceiling retained | now < both use_until <= K14_EXPIRES_AT <= approved_expiry_ceiling <= 2026-10-23T00:00:00Z (23 Oct 08:00 MYT), with use_until <= provider expiry |
| Codex route | Andrew attested automatic ON, personal preference mode, PR-open trigger, exhaustive personal mode on 11 Oct ~22:03 MYT | Linked requesting user/repo access, selected managed route applicability and credit continuation OFF evidence; cloud environment ID remains UNKNOWN, do not invent one or create one by default |
| Protected environments | Main-only author/review environments previously API-verified; environment-only token placement owner-attested; admin bypass limitation recorded | Authorized account seat confirms no protection drift; no broader branch rules or repo-secret fallback |
| Cash | Earlier $0 budget stops and included usage reported | Fresh <=2-hour cash-stop evidence, OFF paid continuation, >=125 included-minute reserve; no fabricated minutes counter |
| Pilot envelope | Template remains unassigned, receipts PENDING | New seed issue >1, unique unused pilot/claim slots, owner-bound Magic author, exact final SHA, two actual final-main comment URLs/body hashes, source/quote and bound limits |
| Hosted runner | Reviewed admission requires Ubuntu24/x86_64/Python3.12.3/ImageVersion20261004.327.1 | Availability remains unproven offline; changed image stops before checkout. Any needed re-pin is a reviewed installation revision and owner gate, never an automatic fallback |
| Launch variables | No variables read or changed during this preparation | Authorized account seat prepares K14_APPROVED_SHA, K14_EXPIRES_AT, K14_PREFLIGHT_JSON, K14_CASH_CHECKED_AT, K14_CASH_STOP_VERIFIED and K14_INCLUDED_MINUTES only with owner authorization; K14_ENABLED true and ready label wait for separate launch approval |

No OPENAI_API_KEY is required by this managed review path. No cash controls,
secret scopes, token lifetimes, two-review/one-revision ceiling, diff caps or
125-minute reserve are relaxed. Bot-authored draft-PR review behavior is the
K-14 experiment outcome, not proof manufactured before this launch.

The agreed adoption order remains K-14 proof -> approved second-repo canary ->
green KEYSTONE/#32 adoption and migration -> safe vendor cleanup. #32 stays draft.
