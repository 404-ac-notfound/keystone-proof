# Installation preparation: mandatory final-main isolation recheck

Magic. Scope authorized by Andrew on 11 Oct after Kobe's static PASS at
`6efb7276e3b45d707458fb59647369c604d5ab98`: fix N1 in the installation revision,
either hard-gate the final-main recheck or delete the green-KEYSTONE alternative.
This separate draft chooses deletion. Frozen PR #3 stays at its checked SHA.

## Code change and launch contract

- Delete the green-KEYSTONE fallback from k14_controller.py and remove the
  keystone_green_main field from the inactive template. Supplying the old field
  cannot restore a bypass; regression tests deliberately try it.
- Both Urahara and Kobe must supply PASS, evidence and controller_sha equal to
  the exact GITHUB_SHA / K14_APPROVED_SHA. Neither checker may be the author.
- After any Andrew-approved installation/merge, both seats recheck that actual
  final main SHA. Candidate receipts cannot be copied to a different SHA.
  The guard additionally requires main == GITHUB_SHA == K14_APPROVED_SHA.
- Missing, partial or stale isolation evidence stops admission before API calls,
  global claim, author invocation, PR publication or review request. Green
  KEYSTONE main has no effect on K-14 admission. Green KEYSTONE remains a later
  prerequisite for #32 adoption/migration.
- No isolation PASS is authored by Magic. Template receipt slots remain PENDING.

## Existing check evidence and corrections to the handoff

[Kobe's static PASS and N1](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6110080967)
and [Urahara's static PASS](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6110063779)
both bind to the frozen candidate only. They do not certify this changed code,
installation/merged main, live provider behavior or final runtime trace.

Two details in Urahara's launch notes must be read against the frozen contract:

1. Provider expires_at may be later than 23 Oct. Actual issuance/expiry metadata
   is still needed, PAT lifetime is at most 30 days from issuance, and
   now < use_until <= K14_EXPIRES_AT <= approved_expiry_ceiling <=
   2026-10-23T00:00:00Z. Andrew accepts and records terminal/cancel/by-use_until
   revoke-and-delete responsibility. The pilot never uses the longer provider
   lifetime as a window extension.
2. K14_APPROVED_SHA must equal the final installed main SHA. The frozen candidate
   SHA is not automatically the launch SHA. Recheck and owner approval must bind
   to final main after the activation installation diff/merge, with the kill
   switch OFF until Andrew's separate launch approval.

Urahara's account/environment/image observations are checker-reported evidence.
No account probe, provider call or isolation assessment was run by Magic here.
A prior image-availability report cannot guarantee the hosted image at launch;
the exact admission guard remains fail-closed.

## Installation status and next gates

This is **installation preparation**, not an installed or activated workflow.
Managed YAML stays .disabled outside .github/workflows; API alternative stays
hard OFF. Main's legacy workflow retirement still needs Andrew-approved merge.
No workflow, credential, environment, runtime variable or launch label changes.

Andrew reviews this delta. The assigned seats assess it, then after approved
installation/merge recheck the actual main SHA. Complete the remaining exact
credential/lifecycle, Codex linked-requester/route/credits-OFF, fresh seed/pilot,
owner-envelope and fresh cash gates. Andrew separately authorizes enablement and
launch. #32 stays draft; proof, canary, adoption and cleanup order is unchanged.

Validation: 36 offline controller tests and 7 locked-runtime tests passed.
Controller regression tests cover injected green status,
zero/one/two final-SHA rechecks, stale receipts stopping before any API call, and
valid final-SHA evidence admitting only the matching main revision. These tests
are synthetic implementation evidence. Independent checks remain with the two
assigned seats.

## Kobe's N1 PASS and F1 follow-up

[Kobe's posted review](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6110337171)
is PASS at `440c947bab6d530e9d63d5674171dbd8e43e0b35`, with 32 independent probes
and 36 controller / 7 runtime tests. It is candidate implementation evidence
only; any new commit needs its own check and final-main checks remain pending.

F1 is corrected in this follow-up: controller_author must be a nonblank string
and may not identify either assigned checker, with case/whitespace normalization
for that comparison. An omitted/null/empty/whitespace/non-string/checker identity
stops guard before API calls. The shipped Magic identity remains unchanged.

Two reported limitations are retained explicitly:

- F2: a moved main is rejected after the create-only global pilot claim, consuming
  that pilot id. No job ref is created. Andrew must use a fresh pilot id; never
  delete/reuse the consumed claim to retry. This remains intentionally fail-closed.
- F3: receipt shape and SHA binding do not authenticate the referenced PASS
  comments. Andrew supplies the non-secret preflight JSON from real checker
  evidence; both seats must verify the actual final-main records. This correction
  does not introduce a self-issued PASS or claim runtime comment verification.

No workflow, lock, credential/config scope or launch control changed in F1.
Validation: 37 controller and 7 locked-runtime tests passed; the new regression
covers author omissions, invalid types, blank values and assigned-checker names,
including case/whitespace variants. These are synthetic tests, not isolation QA.
Urahara owns the independent QA review; Kobe must bind his check to the new SHA.
