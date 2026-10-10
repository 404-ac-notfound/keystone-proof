# Draft: author-independent Codex action review

Status: Andrew review only, 2026-10-10. No activation, merges, account changes,
secret changes, provider calls, or K-14 relaunch authorized by this proposal.
The companion workflow has a `.disabled` suffix outside `.github/workflows`.
Even merging this document would not install it.

## Verification first

The useful claim is supported by a real GitHub issue:
[hide212131/hane #57](https://github.com/hide212131/hane/issues/57),
“ci: trigger Codex reviews with connected GitHub user token.” Its Context records
a live test where `github-actions[bot]` posted the review request but the ChatGPT
Codex integration rejected that actor as not connected to a Codex account.
The proposed repair used a connected user's token only for posting requests.
Read through the GitHub API on 2026-10-10; this is third-party reported evidence,
not an OpenAI promise about every bot on every installation.

Precision: **rejected as an unlinked account**, rather than necessarily silently
ignored. A second measured report, [GENesis-AGI #2808](https://github.com/WingedGuardian/GENesis-AGI/issues/2808),
records 31 account-link refusals following Devin bot requests and none following
81 maintainer requests. These support avoiding bot-posted managed review requests.
They do not prove the cause of keystone-proof's original first-review timeout,
or that bot-authored PRs cannot receive automatic reviews. Comment sender and PR
author are different identities. Do not turn this into a blanket bot-author ban.

[OpenAI's action README](https://github.com/openai/codex-action#example-create-your-own-pull-request-bot)
provides the separate review-job/comment-job pattern and requires a provider API
key. This action runs Codex CLI through the Responses API; it is a different path
from the managed `@codex review` integration. Its `allow-bots` input is not
evidence of the managed integration's behavior. No request comment or user PAT
is needed by this proposal.

## Proposed behavior and boundaries

Install `codex-review.yml.disabled` as `.github/workflows/codex-review.yml` only
in a separately approved activation change. Listen on `pull_request` opened,
synchronize and ready_for_review. Include draft PRs and all authors: there is
no author or association filter. The pinned action's `allow-users: '*'` admits
all triggering actors, including bots; this is confined by the exact repository
and same-repository head check before the action. Fork PRs are excluded.

Two jobs, fresh GitHub-hosted Linux runners:

1. `codex`: GitHub contents/PR/Actions read permissions only; trusted base SHA
   checkout with credentials not persisted; immutable head fetched without
   checking out or executing its changed configuration; Codex `:read-only`
   permission profile with `drop-sudo`. Only static diff review, no test execution.
   The action is last in the job. Head/base staleness, missing key, expired or
   missing cash evidence, duplicate results, reruns, and exhausted attempts stop
   before the model call. A shallow-history merge-base failure also stops.
2. `post_feedback`: PR write permission, no checkout, no API key or Codex;
   receives model output as environment data, never executable code. Rechecks
   open/same-repo/current head AND base, and posts one marked advisory comment.
   Empty/oversized output fails. Existing bot-authored head marker deduplicates;
   report @mentions are neutralized to avoid waking another review bot.

Action pins resolved 2026-10-10: Codex action `bdf19a4a223ec2549a3e2274a0cf61556bc07675`
(v1), checkout `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09` (v5), github-script
`f28e40c7f34bde8b3046d885e986cb6290c5673b` (v7), CLI 0.162.1.
The action [actor check](https://github.com/openai/codex-action/blob/bdf19a4a223ec2549a3e2274a0cf61556bc07675/src/checkActorPermissions.ts)
explicitly accepts `allow-users: '*'` before checking collaborator permissions.

“Every PR” means author-independent event eligibility, **subject to the existing
cash and bounded-pilot stops**. It cannot honestly mean unlimited model calls.
This draft preserves a maximum of two attempts per PR branch, including failed
runs, no rerun retries, expiry 23 October, and 10+2 minute job timeouts. Duplicate
events and blocked runs may consume an attempt; branch reuse stops conservatively.
No counter resets automatically. At most 24 runner minutes for two admitted
attempts per branch; other workflows and PRs still consume the shared allowance.
This is a replacement proposal, not a change to the already-consumed K-14 issue.

There is a separate event-transport limit: [current GitHub documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
says PR opened/synchronize events produced by `GITHUB_TOKEN` require a user to
approve workflows; ready_for_review is not one of those exceptions. Merely
adding this workflow does not establish unattended Actions-bot coverage. Andrew
must decide whether to accept the approval step or separately approve a narrowly
scoped GitHub App/PAT event source. No such credential is requested or created
here. Test transport separately from author eligibility before declaring PASS.

## Cash and secret decision required from Andrew

**`OPENAI_API_KEY` does not exist (owner-reported).** This proposal cannot run.
The action uses API billing; consumer ChatGPT allowance and “Use credits for
reviews OFF” do not constitute an API spending control. GitHub's $0 AI-credit
budget does not cap calls billed directly by OpenAI. A timeout, two-attempt cap,
or an alert-only project budget cannot guarantee $0. OpenAI documents
[separate API billing](https://help.openai.com/en/articles/9039756-managing-billing-settings-on-the-chatgpt-web-and-api-platform)
and [hard spend limits](https://developers.openai.com/api/docs/guides/spend-limits);
hard-limit enforcement can lag and recorded spend can exceed the configured
amount. Therefore a $0 API hard limit alone is not permission to make a billable
review call under the present envelope.

Leave all gates unset/OFF. Do not buy credits, attach billing, or enable automatic
recharge. Under the present $0 instruction, activation stays blocked unless
Andrew establishes an API funding path and enforceable controls consistent with
that instruction, or explicitly approves a revised cash envelope. If that cannot
be established, retain the managed consumer review path for connected human
requests and do not activate this API alternative.

Proposed later setup, after Andrew's yes:

- A separate OpenAI project/service credential scoped to this review task, stored
  as `OPENAI_API_KEY` in the protected `codex-review-owner-approved` environment
  of keystone-proof only. Do not put its value into a PR, chat, logs or files.
- Configure the environment's trusted activation branch and owner approval;
  choose permission restrictions supported by the API provider. Record only
  credential owner, creation/expiry and retirement metadata. No Claude token
  is used by this review job.
- Andrew also approves the model and reasoning effort used by the action;
  set/pin them in the activation PR rather than accepting a moving default.
- Verify actual API financial enforcement, all original GitHub $0/Stop usage
  settings and at least 125 included Actions minutes immediately before a run.
  The repository variables `CODEX_REVIEW_ENABLED`,
  `CODEX_REVIEW_API_ENVELOPE_APPROVED`, `CODEX_REVIEW_CASH_STOP_VERIFIED` must each
  be `true`; `CODEX_REVIEW_CASH_CHECKED_AT` must be an ISO UTC time within one hour
  and `CODEX_REVIEW_INCLUDED_MINUTES` an integer at least 125. These are owner
  attestations and off switches, not an API hard spending cap.
- Disable the old managed automatic review or otherwise explicitly resolve
  double-review usage when activating the replacement; do not change the
  HTTP-400 “All PRs” toggle in this draft. The old poller trusts the managed
  connector bot; this new comment is by `github-actions[bot]` and cannot be
  accepted as a managed verdict. Any K-14 controller integration needs a
  separate provenance/head/run binding change and owner-approved pilot.

## Overdue Claude token retirement

Jarvis reported that `CLAUDE_CODE_OAUTH_TOKEN` still exists in keystone-proof,
last updated 2026-10-09T06:30:31Z. The prior run finished without retirement.
This is an open lifecycle task, not evidence that the value was exposed.

Andrew's next approved retirement should: disable the old K-14 author workflow,
check for/cancel in-flight token users, delete the repository secret, and revoke
the underlying issued OAuth credential through Claude's supported account flow.
Removing a GitHub secret alone does not revoke copies of the issued credential.
If only broader session revocation is available, Andrew chooses its impact.
Verify absence by secret name/metadata and record issuer revocation time or
UNKNOWN pending owner confirmation; never retrieve the value. A future Claude
author pilot requires a fresh, bounded token and retirement on PASS, FAIL,
cancellation or expiry. Do not silently carry the old token forward.

## Acceptance before activation

`python docs/proposals/2026-10-10/check_draft.py` passed: YAML and two-job
permission assertions, fetch-shell syntax, and 27 offline guard/posting scenarios
(missing/stale cash evidence, key absence, forks, changed head/base, duplicate
results, exhausted/failed attempt counts, history pagination, malformed/empty
output, mention neutralization and expiry). These do not prove model quality, API billing enforcement,
GitHub event delivery, environment settings or the missing credential.

After the separate owner gates, one bounded canary must demonstrate a human and
an Actions-bot same-repo PR, synchronize/new head, ready_for_review, fork rejection,
duplicate rejection, stale head/base rejection, missing-key/cash stops and the
two-attempt ceiling. Stay within two reviews per pilot branch; distribute cases
without treating blocked cases as successful reviews. No merge or automatic
repair. The receipt records exact head/base, action/CLI pins, event/actor, run
URL, terminal report, usage evidence and credential retirement.
