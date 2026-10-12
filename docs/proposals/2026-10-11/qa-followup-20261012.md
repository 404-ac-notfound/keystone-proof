# K-14 candidate QA follow-up — 12 Oct 2026

Magic. Historical candidate 7c548e1 received
[Urahara PASS](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6116831548)
and [Kobe PASS with QA follow-up](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6117013677).
This revision changes code and voids their certification. Fresh independent
candidate checks and both actual final-main checks remain mandatory. No merge,
workflow installation, activation, variable/secret/label change or launch.

## Findings resolved

- **QA-1:** the Actions jobs API response was independently read with GET from the
  existing pilot run: object keys are total_count and jobs. The controller's API
  pagination now accepts an explicit page_key for object pages; receipt uses jobs.
  Page/item shapes are validated. Other list endpoints retain list flattening.
  The regression drives actual api() pagination with synthetic gh --slurp pages
  and confirms out/receipt.json and receipt.md are written, containing job records
  and the hard BLOCKED/K23-incomplete outcome. No workflow was run to test it.
- **QA-2:** validate owner JSON object/list/nested-object/seat-string shapes before
  dispatch, including receipt mode. Invalid top-level, null credential/environment,
  unhashable seat and malformed nested records STOP before API/provider actions.
  TypeError and AttributeError are sanitized in the CLI BLOCKED path as additional
  defensive coverage; exception bodies are never copied to the evidence.
- **QA-3:** canonical headline must be its own paragraph. Line-2 retractions and
  other extra opening-paragraph text STOP. Later paragraphs are still scope/context
  for Andrew to read before pinning; no semantic/provenance claim is invented.
  prepare_isolation_record.py performs one same-repo GET and prints the verified
  record/raw-body SHA-256 without normalizing CRLF or adding a newline to the body.
  It never sets variables, writes preflight or grants a PASS independently.
- **QA-4:** QA lock lineage clarified: it is retained from d712b74 and was absent
  on e3bbab1. Workflows and production runtime locks are unchanged from both.
  Merging this candidate would retire main's legacy workflow via the existing
  inert stub. Managed installation is still a separate, explicit reviewed diff.
- **QA-5:** live permissions, providers, credentials, image availability, billing,
  seed/cash and actual final-main behavior remain externally unverified. The
  calculator's seeded failing test remains intentional. No transport PASS claimed.

## Concrete installation proposal — not applied

installation.patch.disabled contains the exact proposed addition of the current
managed template at .github/workflows/k14-managed.yml. It is a review artifact
outside .github/workflows; it is neither executed nor applied by this revision.
It copies the existing template byte-for-byte and adds no permission, provider,
secret or cap changes. A later installation revision must apply the patch within
this same PR #4 line only after Andrew's separate installation authorization.

Proposed order: fix/review candidate → separately approved installation diff
with K14_ENABLED missing/false → reviewed merge/legacy retirement by Andrew →
both final-main rechecks at actual installed SHA → completed owner preflight
and fresh cash/readiness/seed → explicit launch yes and enabled=true last →
Andrew's authorized ready-label tap. PR #3 is superseded as a source; it should
not be merged separately. No PR closure occurs now.

## Validation and remaining input

65 offline tests pass in isolated local Python 3.12/macOS with PyYAML 6.0.2.
Includes realistic multi-page jobs, malformed API pages, owner-shape/clean CLI
BLOCKED files, exact raw CRLF helper hashes and standalone headline regressions.
Local testing is not claimed as installation of the Linux x86_64 QA lock.
Production runtime/workflow/QA locks are unchanged. The installation patch was
checked to reproduce the template exactly without applying it. Diff whitespace
checks pass. These are author implementation checks; reviewer results are separate.

Before launch Andrew still supplies actual PAT creation/expiry, exact OAuth
issuance, use_until/terminal-cancel retirement acceptance, current linked-user/
route/credits-OFF and cash evidence, fresh seed/pilot and exact final-main launch
approval/checker records. No credential values in receipts. Existing author bound
remains 2026-10-22T00:00:00Z; the 23 Oct hard ceiling is unchanged. Runtime image
20261004.327.1 availability must be checked or separately reviewed/re-pinned.

K23 final continuity remains BLOCKED; R1 is still approved and proposed R2 is
[KEYSTONE draft PR #37](https://github.com/404-ac-notfound/KEYSTONE/pull/37).
