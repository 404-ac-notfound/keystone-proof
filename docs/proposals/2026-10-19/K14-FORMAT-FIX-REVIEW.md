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
