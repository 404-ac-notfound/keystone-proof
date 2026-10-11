# Draft review repair — managed K-14 proof first

Updated 2026-10-11 by Magic for Andrew. This supersedes the API-first proposal
in this same draft PR. Nothing is installed, merged, enabled, launched or
provisioned. KEYSTONE #32 stays draft.

Baseline: [joint AGREED closure, KEYSTONE #33](https://github.com/404-ac-notfound/KEYSTONE/issues/33#issuecomment-6103037544),
v2 plus Urahara's item-7 amendment. Andrew assigned **Urahara and Kobe** as the
independent isolation checkers. Magic authors this revision and performs ordinary
implementation validation only; Magic does not perform/certify their check.

## Verification and admitted scope

[hane #57](https://github.com/hide212131/hane/issues/57) reports an Actions-bot
review request rejected because its **comment sender** was not linked to Codex.
It proposes a connected-user request credential. This is reported evidence,
not a universal OpenAI guarantee or an explanation of initial automatic-review
silence on proof PR #2. Request sender and PR author are different identities.

The pilot does not rely on the All PRs toggle (reported HTTP 400) or another
pull_request workflow waking. [GitHub trigger docs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
describe approval-required runs for some GITHUB_TOKEN PR activities. Polling
an absent reviewer does not invoke one.

The eventual eligibility target remains any PR author. **Current admission is
one fresh named seed issue and its one same-repo PR**, two reviews total and one
author revision. No universal unattended coverage is claimed.

## Inactive implementation

Files in `docs/proposals/2026-10-11/`:

- `k14-managed.yml.disabled`: proposed replacement controller outside
  `.github/workflows`; installation requires a separately approved activation.
- `k14_controller.py`: gates, atomic claims, actual request, polling, publication,
  final test and receipt.
- `pilot-config.json`: deliberately unlaunchable non-secret preflight template.
- `environment-status.md`: repo-specific observations and unknowns.
- `test_managed_controller.py`: synthetic offline behavior/permission checks.
- `closure-register.md`: requirement/evidence/follow-up mapping.

One run carries:
`guard → author → publish1 → claim1 → request1 → verify1`.
On findings only:
`revise → publish2 → claim2 → request2 → verify2`.
Final-head test and always-run receipt follow. No leg depends on a second
workflow event. Posting is a real linked-user managed PR review request;
keep its literal invocation phrase out of debate comments/PR descriptions.

Author/revision jobs have read-only GitHub permissions, fresh Claude OAuth,
Read/Edit tools and no request PAT. The hash-verified native Claude CLI avoids the
base-action bootstrap downloads and wrapper PR/comment behavior. They upload only calc.py. Separate
fresh-runner publishers use trusted controller code and publish only calc.py;
model edits to scripts/config/tests are not transported. Model output is data,
never inserted into executable shell text. Poll/test/receipt jobs are read-only.
The PAT exists only in the request POST steps. The external managed Codex review
uses provider review-mode permissions; this workflow does not enforce the API
action's sandbox profile on that external service.

Every controller checkout pins the launch SHA and disables persisted credentials.
Contents write exists only for pilot/attempt claims and publication; PR write
exists only in publication. No merge path. The pilot PR is opened as a draft;
manual managed review of that bot-authored draft is a live-proof question.

## Runtime gates and durable limits

No variables are set by this revision. Owner-provisioned, non-secret variables:

| Variable | Meaning |
|---|---|
| K14_ENABLED | Off switch; missing/OFF stops |
| K14_APPROVED_SHA | Exact controller/launch commit Andrew approved |
| K14_EXPIRES_AT | UTC runtime expiry within the authorized ceiling |
| K14_PREFLIGHT_JSON | Complete owner-approved preflight from the template, original instruction/quote and evidence pointers |
| K14_CASH_STOP_VERIFIED | Existing $0 cash stops verified, no API fallback |
| K14_CASH_CHECKED_AT | UTC account check no older than two hours at each invocation |
| K14_INCLUDED_MINUTES | At least 125 included Actions minutes evidenced |

The external runtime JSON avoids embedding a file's own final commit SHA inside
itself. Approval and checker SHAs must match the exact launch revision. Unassigned
seed, wrong repo/actor, rerun, missing authorization, malformed/expired/extended
expiry, unverified access/retirement and missing bounded credentials stop.
Gates repeat before author preparation, publication, claims, requests and polling.
These are runtime inputs, not magic financial enforcement. For an immediate
mid-flight stop Andrew cancels the run/stops the provider task; changing a
variable cannot recall a request already delivered.

A create-only `k14-claims/<pilot_id>` ref admits the pilot once. Atomic
`k14-attempts/<pilot_id>/1` and `/2` consume slots **before** sending. Failed
or uncertain sends, reruns and duplicate labels never reset them. Changing ids
or deleting refs to bypass limits requires Andrew's new scope.

Each look checks open/same-repo/expected branch, base/head, and 50 files,
1,000 added/deleted lines, 128 KiB full diff. Binary/missing/truncated patches
stop; instruction/lesson Markdown is not silently excluded. Posting rechecks
claim/run, marker and base/head and validates the returned login; no resend.

Poll only accepts the pinned `chatgpt-codex-connector[bot]` after the request,
bound by structured commit identity or full SHA. Time/reactions/green checks/
abbreviated SHAs do not bind. Empty, quota, environment or status output is
NO-VERDICT. Findings dominate clean text; head/base read-back precedes acceptance.
Missing/unsupported managed reviews are BLOCKED, with no retry or API fallback.

Worst-case summed job timeouts: **117 Linux runner minutes** within the planning
reserve of 125. This is not a live remaining counter or final billing evidence;
other work shares allowance. Polls have 30-minute limits/32-minute job caps.

## Scoped credentials — Andrew provisions after approval

| Credential | Placement/scope | Lifecycle |
|---|---|---|
| K14_AUTHOR_OAUTH_TOKEN | Fresh bounded Claude OAuth in keystone-proof only; protected environment k14-author-owner-approved; author/revise steps only | Freshness/expiry evidence; revoke/delete on terminal outcome, cancel or expiry |
| K14_REVIEW_REQUEST_TOKEN | Linked GitHub user's fine-grained PAT, keystone-proof only, minimal PR-comment write/implicit metadata read; protected environment k14-review-owner-approved; request POST steps only | At most 30 days, preferably pilot duration; verify actual posting login; retire after pilot |
| GITHUB_TOKEN | Ephemeral job permissions as listed; never substitutes for the linked-user PAT | GitHub-issued per job |
| OPENAI_API_KEY | Missing, owner-reported; unnecessary for selected managed path | Do not provision for this pilot; API alternative OFF |

No PAT contents write, Actions administration, secrets/variables access or
organization-wide scope; never use it to create PRs. If the minimal supported
permission cannot be established, BLOCKED and Andrew owns the decision. Account
linking/environment/App setup remain owner gates. Values never enter evidence.

**Old CLAUDE_CODE_OAUTH_TOKEN retirement is unverified.** Jarvis earlier reported
present; Urahara's newer evidence reports deletion but lacks verification and
issuer revocation. Do not assert it is definitely still present. Andrew checks
absence by metadata and revokes at issuer; deletion alone does not revoke issued
copies. Broader session-revocation impact is his choice. This draft neither
reads values nor changes/deletes secrets, disables workflows or cancels runs.
A fresh bounded author token replaces the old one; no silent carry-forward.

Runtime bootstrap/runner pins and the protected-environment capability blocker
are detailed in [the fix-up record](../2026-10-11/runtime-and-environment-fixups.md).
The legacy workflow retirement stub is a draft-branch change only; main is not
changed or disabled by publishing this revision. Managed controller files stay
inactive outside .github/workflows. Private GitHub Free environment secrets
are unavailable; the launch remains blocked pending Andrew's capability decision.

## Independent isolation and proof-first order

**Urahara and Kobe** check the exact approved revision, provided neither authored
it. Each records runtime files/refs and a grep/trace showing no KEYSTONE main
path. Their prior checks on 5f25488 are historical; new-revision receipt slots remain PENDING. Synthetic PASS test fixtures are
never real isolation evidence. Magic does not run that assessment.

Missing independent evidence makes green KEYSTONE main a proof prerequisite.
With it, proof may precede repair of KEYSTONE main. Green KEYSTONE is mandatory
before #32 adoption/migrations/cutovers; any baseline re-pin is Andrew's gate.

Order: verify retirement/repo readiness → scoped credentials/reviewed inactive
controller → independent checks → Andrew-authorized fresh-seed run → K-14 PASS
→ approved low-risk second-repo canary → green KEYSTONE/#32 adoption/migration
→ safe vendor cleanup. #32 stays draft/unmerged; PASS grants no merge permission.

## Receipt and validation limits

The same run saves request/reviewer ids/logins, attempt slots, exact base/head/
read-back, verdict/check evidence, final-head test result, controller/config/
environment provenance, old retirement metadata and run/job timings as artifacts
and summary. No transport leg depends on Andrew after his launch tap.

Final Actions usage, billing evidence, owner-touch audit and fresh credential
retirement cannot be verified by a receipt job still running. Its output remains
**BLOCKED pending final evidence**. An independent post-run read/audit may resolve
those fields without supplying a missing transport step. Clean review/tests
alone never self-issue PASS; zero owner transport touches and $0 API spend need
evidence. Preserve FAIL/BLOCKED artifacts instead of retrying.

Offline validation commands:

```sh
python docs/proposals/2026-10-11/test_managed_controller.py
python docs/proposals/2026-10-11/test_locked_runtime.py
python docs/proposals/2026-10-10/check_draft.py
```

These validate controller behavior, job/secret boundaries and permission
structure. They do not invoke models, certify live billing/transport or perform
the assigned isolation check.

## Retained API alternative — OFF

`codex-review.yml.disabled` retains the two-job openai/codex-action design:
read-only model job, separate poster, opened/synchronize/ready_for_review with no
author filter. **Both jobs have hard-false guards**, even if copied. Its helper
now has runtime expiry, a named PR, workflow-global attempt counting and agreed
diff caps. It is not the managed controller or activation-ready. Removing OFF
needs a separately approved revision with funding/financial enforcement,
model/effort pins, protected credential placement and an approved envelope.

[OpenAI's action](https://github.com/openai/codex-action) requires API credentials;
consumer allowance and GitHub's $0 AI-credit budget do not fund/cap API calls.
No automatic fallback, credit purchase, auto-reload, secret provisioning or
provider call is authorized; cash controls remain unchanged.

LeBron's alternative environment wording and VERIFIED/ATTESTED lesson labels
remain recommendations, not new consensus conditions.
