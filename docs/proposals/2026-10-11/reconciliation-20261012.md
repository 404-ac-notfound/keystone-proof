# K-14 reconciliation — 12 Oct 2026

Magic. This inactive PR #4 revision combines both divergent candidates:

- PR #3: e3bbab1697f374cb58528d3d908ca9350ad02b20 — N1 removal, separate OAuth owner-revocation bound, seven-variable envelope/generator, K-23 acceptance gap map and explicit BLOCKED build-complete receipt.
- PR #4: d712b7451ac90d55bfa02516dfd25de26783252c — code-pinned {Magic} author allowlist and exact owner-author binding, canonical same-repo comment URLs/raw-body hashes, strict first-line seat/PASS/final-SHA grammar, malformed API/CRLF regressions, and hash-pinned QA closure.

The hardening is retained, not replaced by PR #3's earlier truthy-evidence gate.
Merged preflight slots remain PENDING with null URLs/body hashes; real receipts
must be supplied. Envelope instructions now include author binding and the full
comment contract. The offline envelope generator validates receipt shape only;
the runtime performs read-only comment-record/content verification before writes
and dispatch. No claim that a comment proves reviewer independence: Andrew owns
reviewer provenance, and Magic authors no isolation PASS.

## Proposed merge order for Andrew

**Use PR #4 as the single combined candidate.** Its reconciliation commit has
both d712b74 and e3bbab1 as parents and contains both lines' changes. Do not
merge PR #3 independently afterward, cherry-pick only one side, or launch either
historical candidate. PR #3 stays draft as a historical source; after Andrew
approves the consolidated path, it can be closed as superseded. No closure or
merge occurs in this preparation.

1. Kobe and Urahara review this combined candidate independently. Their earlier
   checks bind old SHAs only. Kobe's current Claude session was unable to attach
   keystone-proof because its automatic permission review rejected add_repo;
   that access blocker must be resolved through the provider's normal approval
   flow, not bypassed through another fetch route.
2. Prepare the actual workflow installation/legacy-retirement diff within the
   same PR #4 line for Andrew's separate approval, keeping K14_ENABLED OFF.
   The combined revision still leaves managed YAML .disabled outside .github.
   It is not the final installed SHA and does not install anything itself.
3. After any further installation commit, candidate checks become historical;
   review the actual proposed installation diff before approval. After approved
   merge, both assigned seats must recheck the final main SHA. Owner approval,
   canonical comment headline, URLs/raw hashes, GITHUB_SHA and K14_APPROVED_SHA
   must all bind that final revision. No green-KEYSTONE fallback.
4. Complete actual credential dates/use deadlines/retirement, route/credits-OFF,
   fresh seed/pilot and cash evidence. Set variables only on Andrew's launch yes;
   enabled=true last, then Andrew's authorized ready-label tap. No launch now.

Known limitations remain: moved main consumes its create-only claim; never reuse
or delete it. Runner image changes require reviewed re-pin, no fallback. OAuth
provider expiry is unknown, not fabricated; owner bound is 2026-10-22T00:00:00Z
(22 Oct 08:00 MYT). Exact issuance and retirement acceptance are still pending.

K14_TRANSPORT_SUBTEST cannot close K-23. PG plan, Kobe plan verification, Urahara
method approval, Shaq image/QC, Git seat receipts and final-only image delivery
remain implementation gaps. See final-acceptance-alignment-20261012.md.

## Implementation validation

59 offline controller/runtime/envelope tests pass under isolated local Python
3.12 on macOS. Local test environment uses PyYAML 6.0.2; this local test run is
not claimed as installation of the Linux x86_64 QA lock. Existing Linux QA lock,
production runtime/pytest locks, native CLI hash, runner guard, workflow files,
credential permissions and review/revision/diff caps are unchanged byte-for-byte
from both candidate parents. The QA lock is retained from d712b74 only; it was
absent on the e3bbab1 side. Conflict resolution retains PR #4's two N1 tests,
strict parser tests and PR #3's OAuth/envelope/final-acceptance tests. Whitespace
checks pass. Tests are synthetic author implementation evidence, not independent
isolation, real comment verification, billing, model or live workflow proof.

## 12 Oct follow-up after both candidate PASS reviews

Kobe and Urahara both PASSED 7c548e1, candidate only. Kobe then identified QA-1
Actions jobs pagination and QA-2 malformed preflight errors, plus parser/hash-helper
and doc notes. See qa-followup-20261012.md for the corrected candidate and next gates.
These historical PASS comments do not certify any subsequent code change.
