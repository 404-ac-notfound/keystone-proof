# K-14 isolation review fix-ups — 11 October 2026

Magic's implementation revision, **draft only**. Andrew's ruling supplied in this
session: item 7 means **no dependency on KEYSTONE main and no floating refs**;
external actions pinned to full commit SHAs are allowed. Kobe's prior FAIL is
therefore treated as fix-ups, not an unresolved disagreement over external
SHA-pinned actions. This does not grant launch or PASS.

Inputs at parent `5f2548843e3ad167a421d5856c169bfd0974b99c`:

- [Urahara static PASS and four runtime floats](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6105145330).
- [Kobe FAIL and fix-ups](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6104704677).
- Andrew's supplied zizmor finding: the fresh OAuth and review PAT jobs lacked
  protected environments. This finding is addressed without suppressing it.

Both assigned checkers must assess the **new** revision. Their old results are
recorded as history only; the runtime preflight slots remain PENDING. Magic's
validation below is ordinary implementation testing, not their isolation check.

## Changes

| Finding | Draft response |
|---|---|
| Live Claude installer | Removed base-action bootstrap from the managed candidate. Download the native Linux x64 Claude CLI 2.1.296 as data; verify SHA-256 `24972e3bc859fab2b46ed4c1e51f7d6130f06d3bd550811a114640de3370d0de` before chmod or execution. No install.sh or package manager is used for this CLI. |
| Node 18.x | Removed the base-action Node/Bun/Agent-SDK bootstrap entirely. Native CLI invocation retains the bounded Read/Edit author seat. There is no setup-node version range to resolve. JavaScript GitHub actions retain their full-SHA pins and use GitHub's action runtime. |
| Pytest version without hashes | Four exact published wheel URLs and SHA-256s in pytest-requirements.lock: pytest 8.3.5, iniconfig 2.1.0, packaging 25.0, pluggy 1.6.0. Install in a new system-Python-3.12.3 venv with --require-hashes, --only-binary, --no-deps and no cache. Final test uses that venv explicitly; preinstalled pytest cannot satisfy it. |
| ubuntu-latest / runner image | OS label fixed to ubuntu-24.04; every job's first step admits only ImageOS ubuntu24, ImageVersion 20261004.327.1, x86_64, system Python 3.12.3. Missing/changed metadata stops before checkout, actions or controller/provider calls. The API alternative is hard OFF and has the same image guard. |
| Fresh OAuth/PAT outside environment | author/revise use k14-author-owner-approved; request1/request2 use k14-review-owner-approved. Secrets remain step-scoped. Preflight requires verified environment-only storage, main-only deployment policy, source evidence and an unattended protection policy. Repository/organization copies under these names are forbidden; a same-name secret fallback is not acceptable. |
| Floating checkout and other actions in legacy main workflow | PR branch replaces .github/workflows/k14-pilot.yml with a hard-false retirement stub, with no actions, downloads, credentials or author/publisher path. It cannot run the consumed seed-1 design. Main's actual file remains unchanged until Andrew authorizes a merge. The replacement controller remains outside .github/workflows and inactive. |

## What the Anthropic action fetched

Exact inspected source:
[base-action/action.yml at 1d6de8cb0c237e7c15e9e1bdf973826ebae490cc](https://github.com/anthropics/claude-code-action/blob/1d6de8cb0c237e7c15e9e1bdf973826ebae490cc/base-action/action.yml)
and [package.json](https://github.com/anthropics/claude-code-action/blob/1d6de8cb0c237e7c15e9e1bdf973826ebae490cc/base-action/package.json).

That pinned composite called SHA-pinned setup-node and setup-bun, but selected
Node 18.x by default and Bun 1.3.14. It ran bun install --production for
@actions/core, @anthropic-ai/claude-agent-sdk and shell-quote with version ranges;
it did not explicitly use --frozen-lockfile. It then fetched live install.sh to
install Claude 2.1.296 and executed its TypeScript entrypoint through Bun. Optional
plugin/marketplace inputs allow further downloads. A top-level action SHA alone
does not close this bootstrap chain. This revision removes that composite instead
of claiming its SHA freezes these runtime downloads. The old wrapper additionally
has GitHub comment/PR automation that this controller does not use.

The native path uses the official [versioned binary manifest](https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/2.1.296/manifest.json),
read 11 Oct. Its committed hash is authoritative at execution; the manifest is
not fetched or trusted anew during the run. Auto-update and nonessential traffic
are disabled. Safe mode, empty settings sources and strict empty MCP configuration
prevent customizations/plugins/hooks from extending the tool set. The child
receives only its OAuth, PATH/HOME/temp and its isolated config directory; no
GitHub credential, request PAT, API key or alternate-provider routing variables.
CLI flags: [official reference](https://code.claude.com/docs/en/cli-reference);
controls: [official environment variables](https://code.claude.com/docs/en/env-vars).

## Hosted runner pin limitation

The image evidence is GitHub's [Ubuntu24 release 20261004.327](https://github.com/actions/runner-images/releases/tag/ubuntu24/20261004.327)
and [software inventory at exact source commit e3fe113a581eb9a44ca43f479b69f9c93f36df34](https://github.com/actions/runner-images/blob/e3fe113a581eb9a44ca43f479b69f9c93f36df34/images/ubuntu/Ubuntu2404-Readme.md).

A fixed OS label alone **does not pin an immutable hosted image**. GitHub controls
its hosted image rollout. The draft implements an exact-image **admission pin**;
it cannot force GitHub to schedule that dated image. If unavailable, the run
stops. It never silently accepts a replacement. Re-pinning requires a new
reviewed revision and Andrew's gate. If Andrew requires selectable immutable VM
or OCI images instead of this fail-closed admission policy, that is a separate
infrastructure/cash decision; this draft does not provision self-hosted runners
or claim an immutable VM digest. The runner agent/service and remote model
inference remain provider-managed, not a reproducible local OS/model build.

## Protected environment capability — RESOLVED at 21:42 MYT

Andrew reports the repo was made public after Urahara's scan; GitHub metadata
now verifies public visibility. The previous private/Free limitation is closed.
Both named environments were independently read via the public API: exactly
one selected branch policy, main only; branch_policy protection, no reviewer or
wait timer. Admin bypass is enabled and recorded. No protection was modified.
See [updated status](environment-status.md), [owner gate receipt](owner-gates-20261011.md)
and [raw non-secret evidence](owner-environment-evidence.json).

Fresh OAuth/PAT placement, no repository copies and deletion of the old GitHub
secret are OWNER ATTESTED by Andrew at 2026-10-11T13:42Z. Magic did not query
secret metadata, inspect values or authenticate either credential. The PAT is
reported single-repo, Pull requests and Issues read/write, 30 days. No further
publication, plan change or provisioning is needed for this capability gate.

Andrew's about 22:03 MYT update confirms both old issuer tokens revoked and
the new K-14 token kept, plus current repository review settings (OWNER ATTESTED).
Codex cloud environment existence/ID, linked-requester readiness, current credits
OFF and exact new-token UTC metadata remain UNKNOWN/UNVERIFIED. The corrected
controller now separates provider expiry from use_until; a PAT may outlive the
pilot but not exceed 30 days from issuance. Both allowed-use windows and runtime
expiry remain bounded by 2026-10-23T00:00:00Z. No expiry is invented. See
freeze-record.md for the correction and frozen handoff.

The managed controller remains inactive, main retains the legacy workflow, and
new final-revision Urahara/Kobe checks plus Andrew's installation/merge and launch
approvals are still required. See the gate receipt for the exact remaining order.

## Validation and review handoff

Offline controller and runtime tests exercise stops, tampered downloads, secret
boundary enforcement and exact-image admission failures. The retained API
candidate's offline tests remain separate. Local zizmor 1.30.1 (offline, strict collection, no ignores/config) reported zero
findings across managed/API/legacy workflow YAML copies. Prior validation passed 27 controller tests, 7 runtime tests and 33 API
guard/posting scenarios. The expiry-correction freeze passed 33 controller and
7 runtime tests; no workflow YAML/bootstrap/dependency pins changed in that
correction. All four
locked pytest wheels installed successfully into an empty local Python 3.12 venv.
The complete production Python 3.12.3/native author run was not executed. No
model was invoked. Lint cannot prove hosted environment rules,
billing, Codex readiness, runtime isolation, or availability of the pinned image.
The two assigned checkers assess those against the pushed SHA independently.

Order stays: retirement/readiness and capability decisions → scoped credentials
and reviewed inactive controller → Urahara/Kobe exact-revision checks → Andrew's
fresh-seed launch approval → K-14 PASS → approved second-repo canary → green
KEYSTONE/#32 adoption/migration → vendor cleanup. #32 stays draft. No merge,
secret change, activation, paid API fallback or launch is authorized by this PR.
