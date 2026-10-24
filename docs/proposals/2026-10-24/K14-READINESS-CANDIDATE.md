# K14 readiness candidate — inactive, 24 October 2026

Owner direction: finish readiness before importing projects; “Let's get it done.”
Preparation only. No merge, provider call, workflow run, enablement, credential,
account setting, new admission, ceiling extension or project import is performed.

## Changes and objective

Base: PR16 merged main `01ef736eb9514f9386f63c8c8a565ced79ab2ac9`.
Preserve its independent reviews and Andrew's scoped named-mode acceptance.

- Author/revise job caps 12→8 minutes; verify caps 32→14 minutes in installed and
  template workflows. All other workflow content is byte-preserved.
- Poll deadline 30→12 minutes; existing 60-second stable-verdict observation,
  request/head binding, two reviews/one revision and no-rerun rules remain.
- Launch-only budget requires at least 98 minutes: 73 total job caps, 10 queue,
  15 retirement. Check the earliest cash/configuration evidence expiry, credential
  use-until, run expiry, approved stop and code ceiling. Check at offline envelope
  preparation and guard, then recheck after read-only review lookups before the
  first claim write. During active polling, existing freshness gates still apply;
  the full-run reserve is not incorrectly demanded again.
- Normalize CRLF and CR in selected bound findings before writing/validating the
  revision artifact. Original API bodies and review receipt digests are unchanged.
  Artifact mismatch still blocks before author/API/source changes.
- Existing N6 empty/summary-only rejection is retained. The two old timeout
  expectations change from 1800 to 720 seconds; no test case is deleted.

Tradeoff: shorter timeouts can yield more honest BLOCKED outcomes. Ten minutes
of queue reserve cannot guarantee hosted runner availability. Fifteen minutes of
retirement reserve is not permission to defer retirement after a terminal event.
The existing >=125 included-minute gate is intentionally retained.

## Validation

Base: 111 tests PASS. Candidate: 117 tests PASS (six added), using:

```sh
env -i PATH="$PATH" HOME="$HOME" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s docs/proposals/2026-10-11 -p 'test_*.py' -q
```

New evidence covers actual poll→artifact→prepare CRLF/CR flow, appended-text
rejection, exact 98-minute admission boundary, each credential limit, oldest
configuration/cash checks, workflow cap arithmetic and delayed review GETs
leaving insufficient time before identity consumption. Tests are offline with
mocked APIs/clocks; they do not constitute independent verification.

Hosted Python3.12.3, Actions, live reviewers, runner availability, current account
cash/headroom/configuration and retirement readiness remain unverified here.
No actionlint/zizmor result is claimed. A full clean clone was available; no
binary-limited checkout caveat applies to this repository.

## Remaining launch admission — concrete decisions, not approved values

The installed code ceiling remains 22 Oct 08:00 MYT and is expired. The old
configuration-only exception remains limited to pilot K14-20261013-01, seed7,
and 19 Oct 18:00 MYT. Neither is extended by this candidate.

1. Review these implementation changes at the exact candidate head, then obtain
   Andrew's merge decision and actual-main bindings under applicable rules.
2. Establish an available retirement operator and a realistic window; propose a
   new exact UTC ceiling and bound owner revocation deadline together. Do not
   choose a calendar deadline that expires during review by default.
3. Check whether provider readiness/linked-user facts are now exposed. If still
   UNKNOWN, prepare a new narrowly bound one-time admission for a fresh pilot and
   seed, with fresh configuration evidence and final-main review bindings. The
   old exception must not be reused or merely relabelled. Andrew decides this
   concrete new exception before implementation/adoption.
4. After those reviews/decisions, provision fresh environment-only credentials
   under explicit owner authority; record non-secret issuance/expiry/use-until,
   $0 stops, current runner/runtime admission and account evidence. No old claim,
   seed7, PR14 or consumed pilot identity is reused.
5. Rebuild and validate the exact launch envelope; require at least 98 minutes
   remaining at real guard admission, start with an owner-approved event once,
   audit the terminal result, retire credentials promptly and record billing.

No generic “go” substitutes for a named credential or final-head launch approval.
No new owner decision is requested before a reviewable exact-head packet exists.

## Remaining build acceptance and order

K14 is only the bounded code/review transport subtest. After independently audited
live PASS: separately admitted second-repo canary, green KEYSTONE/#32 adoption,
then the reviewed/admitted full creative continuity build and test.

Approved final test remains [KEYSTONE R1](https://github.com/404-ac-notfound/KEYSTONE/blob/main/cabinet/specs/KEYSTONE-CONTINUITY-SYSTEM-FINAL-ACCEPTANCE-SPEC-R1.md):
Andrew request → durable plan → independent Kobe current-plan PASS → Urahara
method PASS → Shaq image execution/QC → final image surfaced to Andrew.
Every stage needs actual Git acknowledgement/completion and revision binding;
zero Andrew-carried messages, manual wakes/resumes, intermediate approvals or
normal intermediate status messages after the single acceptance launch.
No calculator PASS or test count substitutes. No all-provider wake claim follows.
Urahara PR52 remains a separate exact-head review/merge gate; this branch changes
no skill, release archive, doctrine, roster or KEYSTONE repository file.

## Reviewer packet and return

Kobe: independently review this delta against base. Reproduce offline tests;
write probes for expiry boundaries and time lost in review reads, no claim writes
on insufficient reserve, original isolation/credential/publisher/claim controls,
workflow-only timeout diff, and CRLF artifact integrity. Verify the old exception
and expired ceiling remain unchanged. State every scope/runtime limit. Preserve
prior reviews at their actual heads. Re-read current head before posting
`Kobe: <PASS|CHANGES REQUIRED|BLOCKED|FAIL> <full SHA>` on this PR.
Review/comments only; no edits, merge, accounts, launch or provider calls.
Publication of this packet is not delivery or acknowledgement.

Next owner: Kobe for independent candidate review; Magic for admission preparation
and reconciliation. Missing delivery access is a separate blocked lane. Andrew
retains the eventual concrete merge/ceiling/admission/credential/launch decisions.
