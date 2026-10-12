# Installation preparation: mandatory final-main isolation recheck

Magic. Scope authorized by Andrew on 11 Oct after Kobe's static PASS at
`6efb7276e3b45d707458fb59647369c604d5ab98`: fix N1 in the installation revision,
either hard-gate the final-main recheck or delete the green-KEYSTONE alternative.
This installation line chose deletion. PR #3 subsequently advanced to e3bbab1; the 12 Oct unified reconciliation draft now carries both lines. Neither PR has merged.

## Code change and launch contract

- Delete the green-KEYSTONE fallback from k14_controller.py and remove the
  keystone_green_main field from the inactive template. Supplying the old field
  cannot restore a bypass; regression tests deliberately try it.
- Both Urahara and Kobe must supply PASS, evidence and controller_sha equal to
  the exact GITHUB_SHA / K14_APPROVED_SHA. controller_author must be exactly
  Magic, in the code-pinned approved-author list, and match the author named in
  owner_authorization. Adding an author requires a reviewed code revision.
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
  evidence; both seats must verify the actual final-main records. The F1-only
  revision did not claim runtime comment verification. The F3
  follow-up below supersedes that implementation limitation.

No workflow, lock, credential/config scope or launch control changed in F1.
Validation: 37 controller and 7 locked-runtime tests passed; the new regression
covers author omissions, invalid types, blank values and assigned-checker names,
including case/whitespace variants. These are synthetic tests, not isolation QA.
Urahara owns the independent QA review; Kobe must bind his check to the new SHA.

## Urahara QA follow-up: F4 author approval and F3 comment verification

[Urahara's independent QA](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6110568629)
passed isolation and four checks at `0df1a6159f2b78ff47219a3a15bf8de6d1543cd5`,
then identified author aliases (F4), recommended closing F3, and recorded an
unhashed test-only PyYAML installation. That review is historical for this new
revision; both assigned seats must recheck the changed code.

**F4 implemented:** the approved controller-author list is pinned in code to
`{Magic}`. Exact membership and matching `owner_authorization.controller_author`
are required. Unknown authors, checker aliases, misspellings and altered case or
whitespace fail closed. The owner JSON cannot expand this list. The author
identity remains an owner-attested claim; name matching does not discover who
physically authored a commit.

**F3 hardened in code:** each final-main receipt needs a canonical same-repo
GitHub issue-comment URL and the SHA-256 of its exact UTF-8 body. No fabricated
values are filled in the template. On guard admission and each non-receipt
controller CLI stage, read-only GitHub GETs verify both real comments:

- ID and parent issue must match the URL in keystone-proof.
- The publisher must be the code-pinned owner login `404-ac-notfound`; this is
  how both existing seats' review comments are published. A new publisher needs
  a reviewed revision, with no silent fallback.
- The raw UTF-8 body must match its owner-pinned SHA-256. CRLF is normalized to
  LF for parsing only; lone carriage returns are rejected.
- The very first line must be exactly `Kobe: PASS <FINAL_MAIN_SHA>` or
  `Urahara: PASS <FINAL_MAIN_SHA>`, matching the assigned seat. Replace the
  placeholder with the full 40-character approved SHA. No Markdown, backticks,
  padding, suffix, leading blank line or alternative Isolation label is accepted.
- The opening paragraph must contain no other full SHA. Put historical revisions
  and any separate QA/launch status after a blank line; these cannot establish PASS.
- API comment and user payloads must be objects, and the comment ID must be an
  integer. Malformed payloads raise the controller's `Stop` exception.

Missing/unreadable/edited comments, wrong publisher, wrong repository/parent,
wrong seat/SHA or missing PASS stop before claim writes or provider invocation.
Malformed receipt fields still stop pure gates without API calls. These GETs use
existing read permissions; the linked-user PAT remains confined to request POST.
They do not invoke a model, add a review slot, or expand credential scopes.
GitHub comment verification proves existence/content binding, not that a persona
actually performed independent work; Andrew still owns reviewer provenance and
launch approval. No current isolation PASS is inferred or authored by Magic.

**QA dependency closure:** qa-requirements.lock includes the unchanged four
production pytest wheels plus PyYAML 6.0.2's published CPython 3.12 Linux x86_64
wheel URL and SHA-256. The test-only lock was installed in an empty local venv
with --require-hashes --only-binary=:all: --no-deps --no-cache-dir. Production
pytest-requirements.lock, runtime-lock.json and k14_runtime.py are unchanged.

Validation: 48 controller and 7 locked-runtime tests pass in the clean locked QA
venv with an isolated interpreter and no credentials. Only standard PATH and
the unchanged HOME were retained for the existing runtime test fixture. New synthetic probes cover
author aliases and owner-binding, URL/digest requirements, real-comment read
contracts, wrong identity/publisher/seat/SHA/verdict, edits/missing comments
stopping before writes, and CLI evidence failure preventing author invocation.
No live workflow, model, provider, comment-authentication gate, environment or
final-main check was run. Local Python 3.12.14 is implementation validation;
the hosted production interpreter/image admission stays unchanged.

Before launch Andrew supplies real credential issuance/expiry/use_until and
retirement acceptance; real final-main comment URLs/body hashes; approved author
and SHA; target readiness, cash/envelope/seed evidence and launch switches under
separate approval. Both seats recheck final installed main. Image rotation needs
a reviewed re-pin if the admitted version is unavailable; no automatic fallback.


## Kobe FAIL at 205fb9c: strict receipt grammar

[Kobe's independent FAIL](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6110786143)
binds to `205fb9ced09bc63ef1c7dca476cba149f8eb029b`. His hash-locked QA reproduced
44 controller and 7 runtime tests, then found 10 failures among 131 independent
probes. The earlier opening-paragraph/label parser admitted ambiguous verdicts,
stale-SHA PASS text and CRLF scope escapes. Malformed API records raised
AttributeError instead of the intended Stop. Author approval and scope passed.

This draft implements the strict headline contract above and removes the label
fallback. Regressions cover LF and CRLF, FAIL headlines with later PASS text,
withheld/undecided verdicts, stale subject SHAs, different SHAs in the opening
paragraph, raw-versus-normalized digests, lone carriage returns, malformed API
objects and the CLI BLOCKED receipt path. Both existing final-main receipt and
main-equality gates remain mandatory. No workflow, runtime or lock file changes.

The 48 controller and 7 runtime tests are author implementation evidence only.
Kobe's FAIL remains historical evidence until he reviews this new SHA; no current
independent PASS is claimed. Urahara must also review the new revision. Both seats
still recheck the final installed main SHA after Andrew approves installation.


## 12 October reconciliation addendum — superseding handoff

See `docs/proposals/2026-10-11/reconciliation-20261012.md`. The combined draft
inherits the strict F1/F3/F4/F5 review-record and author gates from PR #4 and
the provider-expiry-unknown, owner-bound author OAuth exception from PR #3.
Only author OAuth may use `OWNER_REVOCATION_BOUND` with a recorded
`revoke_by` of `2026-10-22T00:00:00Z`; the PAT still requires real
issuance/provider expiry and a positive lifetime ≤30 days. Runtime admission
enforces the author use-until, but issuer revocation itself is an Andrew action.
The revised receipt explicitly separates K14_TRANSPORT_SUBTEST from the
unpassed K-23 image continuity test. Historical review PASSes on PR #3/#4 are
not valid for the unified revision or eventual final merged main SHA.
