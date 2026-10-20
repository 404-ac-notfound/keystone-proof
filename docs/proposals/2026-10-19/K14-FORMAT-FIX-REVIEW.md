# K14 live-summary compatibility delta

Andrew authorized this scoped fix, offline testing and independent review at
19 Oct 2026 18:01 MYT. The prior attempt is CLOSED-BLOCKED; its unmet objective,
reviews, audit and consumed claim/attempt refs remain intact. No merge or launch
is requested by this candidate.

## Reproduction and behavior

Issue15 was exposed by run39227996178 at controller6f1ce8c. The bot's summary
6263740675 contains an exact full head SHA and completed/no-findings metadata;
the old classifier returns NO-VERDICT because it expects clean prose. The separate
clean receipt6263758228 has only a short SHA and remains unbound after this fix.

The candidate reads the observed codex-review-state:v1 summary directly. Admission
requires the bot login/type, GitHub App ID1144995, canonical same-PR URLs and
positive integer comment ID, creation after the request, ordered nonfuture update,
full head equality and the exact observed schema with actual boolean flags. Only
completed false/false code-review findings flags and an inert security-review block
provide CLEAN. Metadata findings alone wait for actionable bound findings; existing
inline/prose findings take precedence. Pending, malformed, duplicate-key, unknown
version/schema, wrong-head, old or conflicting summaries cannot fall back to a SHA
or clean phrase elsewhere in the body, or borrow clean prose from another comment.

The settle window resets when the observed record snapshot changes or becomes
NO-VERDICT. One unchanged accepted observation must remain present for60s before
emission. Existing per-poll gates and current head/base checks remain.

## Correlation limits

This provider schema exposes no request ID or base SHA. It is correlated through
the request's same-PR endpoint, the single-request protocol, creation after request,
exact full head and the existing current() head/base checks. It is not a provider
request-ID ACK. A summary created before the current request is rejected even if
edited afterwards. Reused summary comments on look2 may therefore remain BLOCKED;
no look2 compatibility or future-schema guarantee is made. A new pilot must include
that limitation in its acceptance envelope; relaxing it requires separate design.

## Files and offline evidence

- k14_controller.py: summary parsing, record construction and stable observation.
- test_managed_summary.py: captured-body regression, publisher/app/PR/head/time and
  schema adversarial cases, findings precedence and mocked poll/settle behavior.
- fixtures/managed-review-39227996178.json: public API snapshots of request,
  summary and short-SHA receipt; original bodies and SHA256 digests preserved.

Original source evidence: immutable8e6e4cf7587028c16e25397ee59e1cfa659616c6,
docs/proposals/2026-10-19/run-39227996178/live-response-sources.json.
The summary body digest is
be38bea9f65afb9dab76b1ed81ff074d598ef82d300de7cec784e042ab199fa2.

Baseline controller blob verified7e7b2c9e5063039208e5fdad22c1c4acd88cb897.
Before changes87/87 offline tests passed. The first candidate passed98/98 on
Python3.12.14 using unittest discovery under docs/proposals/2026-10-11.
All existing test files and their87 tests are unchanged. Tests inject API/clock and perform
no network, provider request, account change or workflow launch. This is not the
locked hosted Python3.12.3 runtime and not an independent review or transport PASS.

Workflow, caps,30min poll deadline,2h freshness, credential gates, old one-time
admission IDs/deadlines and receipt outcomes are unchanged. Main remains untouched.
The expired configuration-only admission is not renewed by this candidate.

## Independent delta review requested

Kobe: verify the exact candidate SHA against6f1ce8c, replay the real fixture and
adversarial cases, inspect the summary-veto/classifier and settle behavior, and
confirm no short-SHA acceptance or gate widening. Preserve prior reviews; review
only this delta. Flag the request-correlation and reused-summary limitations rather
than inferring missing provider fields. No provider calls, account changes, merge,
new launch or claim reset. Post a scoped exact-head verdict on the candidate PR.

The next pilot remains a separately approved proposal; see K14-NEXT-PILOT-PLAN.md.

## Follow-up to Kobe PASS6265091018

Kobe independently passed headff09e330 on19Oct18:26MYT (98 tests onPython3.13.16),
reviewed tree6f214b2e43c7672a996054b0cb2ae4b4bf68f961. Preserve that receipt at its
original head; it is not silently rebound to this follow-up.

N1: corrected proposed caps73min plus10min queues plus15min retirement =98min,
with15:05 latest-launch retained conservatively. Timing remains unimplemented and
outside the parser PASS. N5: validation metadata now covers the register and
distinguishes the original test capture from the later reconciliation.

N4 follow-up: classify now checks CHANGES_REQUESTED before filtering empty bodies.
A bound empty/whitespace change-request review therefore dominates a clean summary;
empty COMMENTED remains non-findings. Two new offline regressions cover this delta.
Request only a narrow follow-up review of these changes, preserving the full prior
PASS. N3 theoretical non-object/float-ID inputs remain documented in Kobe's receipt;
no provider schema or identity admission is broadened.

Follow-up validation:100/100 offline tests pass onPython3.12.14 (87 unchanged,13 new).

## 20 October 10:22 MYT — N6 must be fixed before merge

Andrew selected FIX, not risk acceptance, for residual N6 from Kobe PR16
comment6265666951 and Urahara comment6265970346. His prior merge yes is now
conditional on N6 being fixed and Kobe passing the new exact head. The main K14
session was told HOLD. This candidate push does not authorize a merge or pilot.

The previous classifier's empty CHANGES_REQUESTED precedence remains a veto of
CLEAN, but is no longer enough to emit revision admission. A new pure
`actionable_findings` selector consumes only already-bound review records. It
excludes empty/whitespace bodies, managed summaries (accepted or unsupported),
clean/no-findings prose and priority/header/SHA-only text. Supported nonempty
inline, P0-P3/prose findings or change-request text supply the revision body.
This is syntactic supported-text admission, not a semantic judge of advice.

`poll` turns a findings classification with no such text into NO-VERDICT, resets
its settle window and keeps waiting within the unchanged 30-minute bound for
late inline/prose findings. If none arrives it ends NO-VERDICT, so the workflow
never schedules its revision job and the run remains BLOCKED. A clean summary
beside the empty request cannot turn that veto into CLEAN or revision input.
The findings artifact contains only the selected actionable text, not every
record body. Clean or timed-out outcomes write an empty artifact.

`prepare --look 2` independently requires actionable text from the stored bound
records and an exact (outer-whitespace-normalized) match to the downloaded first
findings artifact, before `current`, source API reads or author input writes.
An empty, summary-only or mismatched artifact ends BLOCKED. It passes only the
validated findings text to the author; the existing one-revision cap remains.

Eleven new offline tests in `test_actionable_findings.py` cover both required
negative cases through the real poll and actual `out/findings.md`: empty request
alone, and empty request beside the captured clean summary (each also whitespace
only). They cover clean/no-findings change-request prose, findings arriving late
and settling for60s, positive prose change requests, marker/header/SHA-only
bodies, summary bodies containing priority annotations, prepare-stage negative
cases before any API or author write, mismatched artifacts, and a valid prepare.
All 100 existing test cases/files at90b885b remain unchanged; final candidate
has111 passing offline tests onPython3.12.14. APIs, clocks and author operations
are mocked; test processes are launched without credential environment variables.
The locked hosted3.12.3 runtime is not exercised. pytest/actionlint/zizmor are not
installed in this session; existing workflow/runtime/seed files are byte-identical.

No workflow, cap, identity binding, schema, timing, admission, credential, variable,
launch, claim or seed change is made. K14 stays off; the existing expired admission
and proposed/unimplemented timing envelope remain unchanged. No live-variable or
credential inspection occurred. N6 is IMPLEMENTED, pending Kobe's independent
exact-head verification; no prior review is rebound and no transport PASS claimed.
