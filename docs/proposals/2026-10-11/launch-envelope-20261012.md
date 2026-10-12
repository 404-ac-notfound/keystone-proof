# K-14 launch envelope for Jarvis — 12 Oct 2026

Magic. Relay: `KEYSTONE-K14-RELAY-20261010`. This reconciled candidate also retains PR #4 hardening (d712b74). Andrew reopened frozen draft PR #3
at `6efb7276e3b45d707458fb59647369c604d5ab98` to fix Kobe N1 and prepare this
handoff. This revision authorizes draft preparation/push only. No merge,
installation, activation, variables, secrets, seed creation or label launch.

## Current installation state (supersedes earlier preparation-only wording)

Andrew approved the installation revision and review dispatch on 12 Oct.
The installed workflow is now .github/workflows/k14-managed.yml on draft PR #4;
main remains unchanged, K14_ENABLED remains unset, and merge/launch remain separate
owner gates. Earlier statements below that no installation occurred describe
the earlier envelope-preparation phase, not the current draft-branch state.
The seven-variable contract is unchanged and now read by the installed copy.
Kobe's dffc80e PASS is candidate-only; current-head and actual final-main checks
remain required.

## Final acceptance scope and hard gap

[Final acceptance alignment and full PASS contract](final-acceptance-alignment-20261012.md)
records the owner-approved R1 spec at immutable KEYSTONE commit 39e25bb. It requires
Kobe current-plan verification, Urahara method approval, **Shaq image generation/QC
and Git receipt**, then exactly one final image shown to Andrew with zero
intermediate status messages. Those stages are not implemented by the calculator
pilot. Therefore this envelope is **K14_TRANSPORT_SUBTEST only** and **BLOCKED for
K-23 final acceptance**. Do not set it for the final image test or close the build
on a calculator/review PASS. A future reviewed implementation/envelope must cover
all stages and metrics before a final-test launch. No image is generated now.

## N1 and revision binding

The green-KEYSTONE-main alternative is deleted from the controller and template.
Urahara **and** Kobe must each provide PASS with evidence and `controller_sha`
equal to the **actual final merged main SHA**, independently of author Magic.
Each final-main check records the files and refs read at runtime and a grep/trace showing no KEYSTONE main path. Missing, stale or partial receipts or isolation evidence stop the run. The two PASS comments on
6efb727 are historical evidence only:
[Urahara](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6110063779),
[Kobe/N1](https://github.com/404-ac-notfound/keystone-proof/pull/3#issuecomment-6110080967).
This update voids their certification of the candidate. No checker was contacted
or impersonated. Recheck after the separately approved installation/merge is a
hard gate; never set `K14_APPROVED_SHA` to the old frozen SHA or this draft head.

## Credential dates

Andrew's relay states: **“Andrew revokes by 2026-10-22.”** Claude OAuth provider
expiry is not shown on claude.ai. Preserve `author_credential.expires_at = null`;
record an `OWNER_REVOCATION_BOUND` separately. This draft chooses the conservative
cutoff **2026-10-22T00:00:00Z (22 Oct 08:00 MYT)**, within the stated calendar day.
It is an owner revocation commitment, not a provider expiry or proof of token
validity. No token is decoded or probed. Early provider expiry still prevents
successful use. The generator caps the entire launch envelope at this bound.

The gate accepts unknown expiry **only for author OAuth** with named launch owner,
explicit bound basis, UTC revoke-by and evidence. Exact issuance, approved
use-until and terminal/cancel retirement acceptance remain necessary. The PAT
still requires actual `created_at` and `expires_at`, supplied by Andrew from the
GitHub token page (including timezone/UTC conversion). A positive PAT lifetime
must be ≤30 days from issuance; it may expire after the pilot. Never substitute
the OAuth bound or pilot cutoff for PAT provider expiry. Andrew revokes and deletes
both credentials on terminal outcome, cancellation or by each `use_until`,
whichever occurs first. Gates do not perform provider revocation.

## Exact Actions variable envelope

Repository: `404-ac-notfound/keystone-proof`. All values are strings. These are
**all seven** variables read by `k14-managed.yml.disabled`; no additional GH_REPO,
GITHUB_SHA or run-attempt Actions variables are needed (workflow/GitHub supply them).
The JSON companion is a non-executable preparation manifest, not a ready set-file.
Null entries are unresolved and must never be sent to GitHub.

| Name | Launch value / required resolution |
|---|---|
| `K14_ENABLED` | `true`, set **last**, only on Andrew's explicit launch yes; keep missing/`false` until then |
| `K14_APPROVED_SHA` | Actual final merged/installed main's full 40-character SHA, equal to owner approval and both fresh checker receipts |
| `K14_EXPIRES_AT` | Proposed `2026-10-22T00:00:00Z`; Andrew approves this or an earlier deadline; shorten if either credential's allowed-use/provider bound requires it |
| `K14_PREFLIGHT_JSON` | Exact compact JSON generated from the completed owner preflight described below; no placeholders or invented evidence |
| `K14_CASH_CHECKED_AT` | Actual fresh verification time in UTC `YYYY-MM-DDTHH:MM:SSZ`, never a preparation timestamp |
| `K14_CASH_STOP_VERIFIED` | `true` only after fresh $0 cash-stop, headroom and paid-continuation-OFF evidence |
| `K14_INCLUDED_MINUTES` | `125` reserved included minutes, only if at least that amount is verified available; a greater verified reserve is also allowed |

Cash evidence must be ≤2 hours old at **every gated step**. The 125-minute total
job timeout ceiling can exceed that freshness window; a late step fails closed.
Do not future-date evidence, silently refresh it or bypass the gate to finish.

## Complete K14_PREFLIGHT_JSON

Copy `pilot-config.json` outside the tracked code and retain its verified historical
records, environment names, repository/logins, caps and ceiling. Complete these
fields from actual evidence:

- `pilot_id`: proposed `K14-20261012-01` (preparation only). Before assignment,
  verify no `k14-claims/<pilot_id>` or `k14-attempts/<pilot_id>/1` or `/2` exists.
  Use another newly approved unique id if any exists. Do not delete consumed slots.
- `seed_issue`: a separately authorized **fresh issue >1**, integer, with no existing
  `job/<seed_issue>` branch. No issue number is invented or created by this draft.
- `owner_authorization`: `{ "source": <Andrew's authenticated launch-yes reference>,
  "quote": <exact launch approval>, "approved_sha": <final main SHA>, "controller_author": "Magic" }`.
  Setup/merge approval does not fill this field. Approval must cover the exact
  seed, pilot, deadline, envelope and revision.
- `independent_isolation`: exactly two entries, seats `Urahara` and `Kobe`, each
  `status: "PASS"`, `controller_sha: <final main SHA>`, and its own canonical same-repo issue-comment evidence URL plus `comment_body_sha256` of the exact raw UTF-8 body. Each comment must start exactly `Urahara: PASS <full final main SHA>` or `Kobe: PASS <full final main SHA>`, as appropriate; publisher must be `404-ac-notfound`. No Markdown/padding/suffix/leading blank line or second SHA in the opening paragraph. Record the raw-body hash after the actual comment is posted; do not normalize line endings when hashing. The runtime verifies these records with read-only GETs before writes/dispatch. Owner author identity must be exactly `Magic`, in the code-pinned allowlist and owner authorization. No invented hashes or receipts.
- `environment`: `status: "READY"` with source/time/evidence for the selected managed
  review route. An environment id may remain null if that route needs no cloud
  environment; record route applicability rather than inventing an environment.
- `connected_user_access: "VERIFIED"`, `managed_review_configuration: "VERIFIED"`,
  `paid_review_credits: "OFF_VERIFIED"`, supported by current source/time/evidence
  (additional evidence fields are allowed). Historical repository settings alone
  do not establish linked-requester access or live bot-draft-PR support.
- Both credentials: actual `created_at`, owner-approved `use_until` no later than
  the envelope stop, non-secret evidence and terminal/cancel retirement acceptance
  (`owner: "404-ac-notfound"`, `on_terminal: true`, `on_cancel: true`, evidence).
  Author keeps `expires_at: null` and the recorded separate revocation bound.
  PAT `expires_at` is Andrew's actual provider expiry; it must cover its use-until.
  Exact author issuance remains unresolved; the approximate old chat time is not
  promoted to provider metadata.
- Reconfirm the recorded protected environments remain main-only and environment-only
  at launch; maintain author/review separation. Keep old OAuth retirement evidence.
  Bounds stay two reviews, one author revision, 50 files, 1,000 lines, 131,072 bytes.

No credential values go into this JSON or launch receipt. Secrets remain
`K14_AUTHOR_OAUTH_TOKEN` only in `k14-author-owner-approved`, and
`K14_REVIEW_REQUEST_TOKEN` only in `k14-review-owner-approved`. No repo-secret fallback
or API key. No secret changes are part of this handoff.

## Jarvis preparation and future authorized sequence

1. Obtain missing PAT/provider dates, exact OAuth issuance, route/credits readiness,
   retirement acceptance, fresh seed/pilot, final-main checks and Andrew's exact
   launch approval. Separately approved installation must retain the retirement
   stub and leave the kill switch OFF. This draft installs nothing.
2. Prepare the completed non-secret owner JSON, then use the offline tool:

   ```sh
   python3 docs/proposals/2026-10-11/prepare_launch_envelope.py \
     --preflight completed-owner-preflight.json \
     --main-sha "$FINAL_MAIN_SHA" \
     --expires-at 2026-10-22T00:00:00Z \
     --cash-checked-at "$ACTUAL_CASH_CHECKED_AT" \
     --included-minutes 125 --cash-stop-verified \
     --output launch-variables.json
   ```

   Supply actual full SHA and cash time; no placeholders may reach output. The tool
   checks local preflight/gates and emits the exact seven strings, without GitHub
   calls, setting variables or invoking a workflow. It does not verify the truth
   of owner/checker evidence or live main. Do not use synthetic test fixtures.
3. On Andrew's launch yes only: independently read back main and current settings,
   confirm main matches approved SHA, final checker receipts match, cash is fresh,
   slots are unused, credential metadata/bounds are accepted, and the locked hosted
   image policy is still applicable. Any discrepancy stops preparation/launch;
   image re-pin requires a new reviewed revision and checks, no silent fallback.
4. Keep `K14_ENABLED` missing/`false` while setting the other six reviewed strings.
   Read back all six byte-for-byte against the generated file. Recheck main and
   deadline/cash freshness, then set `K14_ENABLED = true` last. This is a future
   authorized action, not an instruction to set anything during draft preparation.
5. Andrew performs the separately authorized fresh-seed `ready` label tap: the
   controller requires event sender `404-ac-notfound`. Jarvis must not substitute
   its own posting identity. No reruns, paid API fallback or extra review request.
   Record runtime refs, review/head/readback, usage and actual credential retirement;
   unresolved final evidence stays BLOCKED.

Current launch disposition: **NOT YET**. PAT dates, exact issuance, actual final
main SHA/checker evidence, fresh seed/readiness/cash and launch yes are unresolved.

## 12 Oct QA follow-up — current strict receipt contract

The canonical Seat: PASS full-SHA first line must be its own paragraph, followed
by a blank line before any body text. Multi-line opening paragraphs stop, including
retraction text. Later paragraphs remain owner-read scope/context; the parser
does not establish reviewer provenance or semantic approval of the whole body.
Use prepare_isolation_record.py --url <canonical-comment-URL> --seat <seat>
--sha <actual-final-main-SHA> to read one comment and emit its exact raw UTF-8
body hash/record. The helper performs one scoped GET and validates identity,
publisher and headline; it does not write preflight, set variables or certify
independence. Candidate comments cannot be reused as final-main receipts.
