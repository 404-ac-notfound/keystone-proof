# Environment and capability record — 11 Oct 2026, 21:48 MYT

Magic's read-only verification and Andrew's authenticated owner report at
**21:42 MYT / 13:42 UTC**. No setup, secret change, review request or launch by
Magic. Evidence: [owner gate receipt](owner-gates-20261011.md) and
[public API metadata](owner-environment-evidence.json).

## GitHub capability and credential environments

The earlier private/Free capability blocker is **RESOLVED**: repository metadata
now reports `private: false`, `visibility: public`. No paid plan or further
visibility change is required for public-repo environment secrets under the
[current GitHub capability rules](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

| Environment | ID | Verified policy | Protection observation |
|---|---|---|---|
| k14-author-owner-approved | 24011236134 | One custom deployment policy: branch main; no tag or wildcard policy | branch_policy only; no reviewer or wait timer; can_admins_bypass=true |
| k14-review-owner-approved | 24011239056 | One custom deployment policy: branch main; no tag or wildcard policy | branch_policy only; no reviewer or wait timer; can_admins_bypass=true |

The environments exist and their main-only restriction is **API VERIFIED**.
They use selected-branch policy, not the protected-branches-only option that can
admit all branches when no branch protection exists. Their configured rules
introduce no deployment reviewer/wait-timer touch during the pilot. Admin bypass
is enabled; that limitation is recorded, not silently changed. Main-only policy
is not a separate claim that main itself has branch protection.

Secret placement, no same-name repository copies, fresh author OAuth and old
secret deletion are **OWNER ATTESTED**, not independently queried by Magic:

- Author environment: K14_AUTHOR_OAUTH_TOKEN from a fresh claude setup-token.
- Review environment: K14_REVIEW_REQUEST_TOKEN, fine-grained, keystone-proof
  only, Pull requests and Issues read/write, 30-day validity.
- No repository-level copies of either fresh credential; old
  CLAUDE_CODE_OAUTH_TOKEN deleted.

No token values were read or authenticated. Public environment metadata does
not establish secret contents, expiry or issuer-side revocation. The old token's
issuer revocation remains UNKNOWN. Exact new-token UTC expiries remain UNKNOWN.

## Codex environment and review-path status

| Repository/path | Current verified fact | Status still unknown |
|---|---|---|
| KEYSTONE Codex cloud interaction | The connector's historical issue #33 response asked for an environment on 10 Oct at 17:21:57Z | Present Codex cloud environment existence/ID; this is not a keystone-proof review result |
| keystone-proof Codex cloud environment | No Codex-account environment inventory is exposed by the available tools; no owner environment report was supplied for this service | Existence/ID UNKNOWN; not asserted absent |
| keystone-proof managed PR review | Earlier Jarvis report: auto ON, On PR open, Follow personal preferences, personal auto OFF; All PRs save HTTP 400 | Current repository connection, linked-user access/configuration, credit continuation OFF and bot-draft-PR support UNVERIFIED |

Historical [connector response](https://github.com/404-ac-notfound/KEYSTONE/issues/33#issuecomment-6100189317)
is issue-level evidence only. PR #2's fetched discussion contains an Actions
receipt, not an independent Codex verdict. No test review was requested now.

[OpenAI's Code Review guide](https://learn.chatgpt.com/docs/code-review), fetched
11 Oct, says cloud review does not require creating/managing a cloud environment.
Its [GitHub integration guide](https://learn.chatgpt.com/docs/third-party/github)
requires a connected repository and access to review settings. Therefore a new
Codex cloud environment is not a blanket prerequisite. The selected target
review route still needs an account-level readiness record; evidence that a
cloud environment is unnecessary for that verified route can satisfy the
applicability field. The two GitHub credential environments above do not prove
Codex-account readiness.

No current account read is available here for Codex environment inventory or
review settings. Record these as UNKNOWN, and let an authorized read-only account
seat supply target connection/settings and applicability evidence without
invoking a review. A blocked/unsupported review during the authorized pilot must
produce BLOCKED, never a retry or paid API fallback. OPENAI_API_KEY remains
unnecessary for the selected managed pilot; the API alternative is hard OFF.

See owner-gates-20261011.md for the exact remaining launch conditions, including
the credential-expiry mismatch, independent checks and approved installation.
