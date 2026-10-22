# Next K14 pilot proposal — NOT LAUNCHABLE

## Status and owner decision

Andrew approved the prior attempt's CLOSED-BLOCKED disposition and scoped
fix/offline/independent-review work on19Oct18:01MYT. Launch remains prohibited.
K23 transport-dependent activation stays held. No credential, label, workflow,
settings, main-branch or consumed-identity change is part of this proposal.

## Candidate and acceptance

First review the compatibility delta against6f1ce8c. Candidate PASS does not count
as an installed-main binding or a live test. After required reviews and a separately
authorized merge, bind the actual main SHA under the reviewed admission rules.

Proposed pilot objective: show actual Claude authoring and actual commit-bound
managed review accepted by the controller, followed by finalcheck on that same
head/base, within the $0 spend ceiling and all bounds. Provider completion alone
does not satisfy it. Whole KEYSTONE creative continuity and K23 activation remain
separate acceptance criteria.

Completed code reviews and source provenance remain preserved; the new delta
requires independent review. Required assigned-seat/main bindings are determined
by the concrete new admission amendment, not silently waived here.

## New identities and evidence

- Provisional new pilot ID K14-20261020-01 (proposal only); fresh seed/PR/claim/
  attempt refs to be assigned after authorization. Never reuse seed7, PR14,
  K14-20261013-01 or their consumed refs.
- Fresh least-privilege author OAuth and request PAT only after owner approval.
  Previously used credentials are revoked. No secrets in Git or account receipts.
- New account evidence collected after the reviewed packet and operator are ready;
  actual check times precede preflight completion. Preserve $0 budgets, paid
  continuation OFF and environment-only secrets; no repository fallback.
- Codex environment readiness and linked username remain UNKNOWN unless actually
  exposed. The19Oct one-time configuration admission expired. A new scoped owner
  decision plus reviewed amendment is required if these UNKNOWNs persist.
- Proposed outer stop20Oct18:00MYT, earlier than the installed22Oct08:00MYT code
  ceiling. This is a proposal, not an extension or use authority.

## Timing is a separate unresolved gate

Existing worst-case job timeouts sum117min before queue/provisioning variation.
The2h evidence window starts at the oldest check, before preflight; a15min
retirement margin cannot safely fit that path. Do not launch this unchanged timing
profile simply because the parser regression passes.

Proposed narrow timing delta for review: author/revise job caps8min each (currently
12); each poll deadline12min (currently30), verify jobs14min (currently32); retain
all other caps. Total job caps would be73min including receipt; reserve10min for
queues/provisioning and15min for retirement =98min. This trades a greater chance
of an honest BLOCKED timeout for a feasible2h envelope. The only observed provider
response was about77s after request; one run is not a reliability estimate.
No timing code/workflow changes are implemented by the format-fix candidate.

If approved and independently reviewed, a provisional20Oct schedule is:

- Oldest account check no earlier than14:55MYT; complete packet/preflight by15:00.
- Launch no later than15:05 only if all required validity windows have at least
 98min remaining at the actual label action; otherwise stand down.
- Ordinary2h freshness would stop use no later than16:55 for that batch. The
 outer18:00 limit does not extend freshness. Credential use bounds may be earlier.
- The15:05 operational latest-launch remains conservative: an oldest14:55 check
  leaves110min at15:05,12min beyond the corrected98min envelope. The budget alone
  would permit15:17 under those exact facts; this proposal keeps15:05 and does not
  authorize using that extra slack as a later launch.
- Recheck full budget at actual launch. Queue overruns still fail closed at the
 existing freshness/credential/stop gates; do not refresh mutable evidence midrun.

This proposal deliberately narrows timeouts rather than extending evidence age.
The timing delta, including a concrete launch-budget check/operator checklist,
requires review and inclusion in the next exact-head owner-approved envelope.

## Runtime, retirement and disposition

Retain at most2 reviews/1 revision, existing diff caps, no retry/resend, no smoke
task, no paid fallback, stable60s verdict observation and final head/base checks.
Reused-summary look2 may remain unsupported; record that as BLOCKED rather than
relaxing commit/request binding or overriding a verdict.

Jarvis must be present for terminal/cancel/deadline retirement: enable=false with
readback, delete both environment secrets, revoke both issuer credentials, verify
absence, report exact times. Proposed15min reserve is an operational allowance,
not permission to retain credentials after terminal. Begin retirement promptly.
An automated retirement path is not claimed or introduced here.

Collect immutable terminal artifacts, current billing/usage and owner-touch
accounting; obtain independent terminal audit. Assess the same exact run/head.
An Actions badge, canned bot reply or offline test count never supplies PASS.
Delayed metering remains a later dated followup, with an explicit assigned holder.

## Approval sequence and owner actions

1. Scoped format-fix independent delta review (authorized now).
2. Review timing delta and next one-time UNKNOWN-admission design. Andrew decides
   those concrete changes and the eventual merge; neither is pre-approved here.
3. Produce exact merged-main bindings and the final pilot envelope with actual
   fresh seed, approved stop, caps, evidence and retirement operator.
4. Andrew explicitly approves credential provisioning and that bounded launch.
5. Jarvis executes account steps; Magic verifies transport and disposition.

No account action is needed from Andrew during the present offline phase.
