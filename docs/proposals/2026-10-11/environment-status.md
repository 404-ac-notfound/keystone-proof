# Codex readiness record — 2026-10-11

Read-only evidence. No environment created/changed; no review request sent.

| Repo | Environment evidence | Review configuration | Current readiness |
|---|---|---|---|
| 404-ac-notfound/KEYSTONE | Connector said “create an environment for this repo” at 2026-10-10T17:21:57Z / 11 Oct 01:21:57 MYT on issue #33 | Earlier supplied screenshot showed Automatic review ON; not rechecked live here | Prerequisite observed for that issue interaction; present environment existence/id UNKNOWN |
| 404-ac-notfound/keystone-proof | No target environment inventory exposed by the available GitHub connector; existence/id UNKNOWN | Jarvis 10 Oct report: Automatic review ON, On PR open, Follow personal preferences; personal auto OFF; All PRs save HTTP 400. Current live settings UNVERIFIED | Managed bot-PR coverage UNPROVEN; readiness preflight PENDING; launch BLOCKED |

Direct evidence: [connector comment 6100189317](https://github.com/404-ac-notfound/KEYSTONE/issues/33#issuecomment-6100189317),
login `chatgpt-codex-connector[bot]`. Body/time re-read through GitHub REST on
11 Oct. This issue response does not prove bot-PR review or keystone-proof's
environment absence, and does not prove today's KEYSTONE settings. No account
environment list or secret values were queried.

Current official pages opened 11 Oct:

- [GitHub review guide](https://learn.chatgpt.com/docs/third-party/github): a
  connected repository, access to review settings and the managed PR entrypoint.
  The fetched current page does not make a separately managed environment a
  universal review prerequisite.
- [Code Review guide](https://learn.chatgpt.com/docs/code-review): automatic cloud
  review does not require creating/managing a cloud environment. A cloud coding
  task and repository-triggered review are distinct paths.

These docs qualify blanket claims that every review requires a newly created
environment. They do not establish this account's selected path or override the
actual connector response or #33's agreed preflight. Record environment status
and review-path access/configuration separately; Andrew decides account changes.
Do not create an environment automatically or silently relax the launch gate.

Before launch, an authorized seat supplies target-repo connection/access,
environment status/id or verified applicability evidence, linked-user identity,
exact review settings, current included allowance and paid-credit continuation
OFF, with source/time. Runtime preflight remains UNKNOWN until supplied. A READY
attestation must explain the chosen route; it need not mean a newly created
environment if the verified route does not require one.

Urahara/Kobe isolation checks and issuer-side OAuth retirement are separate
pending preflight entries. Missing OPENAI_API_KEY belongs only to the hard-OFF
API alternative. This record grants no setup, credentials, spend or activation.

## GitHub credential environments — separate prerequisite

The draft now names k14-author-owner-approved and k14-review-owner-approved.
These are proposed GitHub credential environments, distinct from a Codex cloud
environment. No creation or protection was observed/performed. PR metadata
confirms private keystone-proof; supplied account evidence says Free. Environment
secrets on that combination are unavailable under the current documented plan.
See runtime-and-environment-fixups.md for primary source and Andrew's capability
gate. Preflight remains unlaunchable; no repository-secret fallback is allowed.
