# K-14 draft freeze — 11 Oct 2026

> Superseded for current launch preparation by [12 Oct relay and envelope](launch-envelope-20261012.md). Andrew reopened 6efb727 for N1; the green-main bypass is removed and OAuth unknown expiry uses a separate owner revocation bound. Historical freeze/evidence below is retained.

Magic. Andrew authorized the expiry correction and freeze following his owner
report at approximately 22:03 MYT / 14:03 UTC. Parent:
`072b505390a464fd80a594148f3529d4a6e6b795`. The immutable candidate commit SHA is
recorded in [draft PR #3](https://github.com/404-ac-notfound/keystone-proof/pull/3)'s
description and Andrew's chat receipt after push. No further candidate changes
by Magic without Andrew reopening the revision. This is a review freeze, not a
branch-protection change, independent isolation PASS or launch authorization.

## Expiry contract

| Field | Meaning and enforced bound |
|---|---|
| created_at | Actual provider issuance UTC, not the approximate chat report; must be no later than now |
| expires_at | Actual provider expiry UTC; must cover use_until; may outlive the pilot |
| request credential lifetime | Positive expires_at minus created_at, at most 30 days; never measured from invocation |
| use_until | Owner-approved allowed-use and revoke/delete deadline; now must be strictly earlier; no later than K14_EXPIRES_AT |
| K14_EXPIRES_AT | Runtime stop; no later than approved_expiry_ceiling |
| approved_expiry_ceiling | No later than hard ceiling 2026-10-23T00:00:00Z, preserving the original UTC date boundary (23 Oct 08:00 MYT) |
| retirement | Andrew accepts revoke/delete on terminal outcome, cancellation or by use_until, whichever is first; owner/evidence/terminal/cancel acceptance required |

Thus an honestly reported 30-day PAT expiring in November can be used for a
shorter October pilot. No credential's actual expiry is rewritten to the pilot
end. Shorter use_until stops both author and request paths at the next gate.
Gating is not automatic provider revocation: Andrew owns and records actual
retirement. No secret changes were made. Real issuance/expiry/use_until and
retirement acceptance remain null/missing in the inactive preflight template.

## Evidence and validation

- Andrew OWNER ATTESTED: GitHub old secret deleted at 21:42 MYT; both inference-only
  9 Oct issuer tokens revoked at claude.ai Authorization tokens; fresh K-14 token
  created about 21:41 MYT kept, reported about 22:03 MYT.
- Andrew OWNER ATTESTED current keystone-proof settings: Automatic review ON;
  Review Follow personal preferences; Trigger On PR open; Exhaustive review Follow
  personal preferences. Live bot-draft-PR coverage and linked requester access
  are not inferred from settings. Cloud environment existence/ID stays UNKNOWN.
- 33 offline controller tests and 7 locked-runtime tests passed for this revision.
  Synthetic fixtures are implementation tests, not isolation evidence or live
  provider/billing validation. Prior API/lint/wheel validation is retained as
  historical validation of unchanged files; no new model or workflow run.

## Remaining owner gates, in the agreed order

1. Complete exact fresh-credential metadata/lifecycle acceptance; linked-requester
   access, route applicability and current credits-OFF readiness evidence.
2. Urahara and Kobe independently inspect this exact candidate, then bind/recheck
   the actual final main SHA after an Andrew-approved installation revision.
   Magic does not perform their isolation check. Historical 5f25488 checks do not
   certify this candidate.
3. Andrew approves installation/merge/legacy retirement separately. The managed
   workflow stays .disabled outside .github/workflows; main and its legacy
   workflow remain unchanged. API alternative hard OFF. Main-only credential
   environments are not broadened to test draft branches.
4. Complete fresh seed (>1)/pilot/envelope, exact approved main SHA and fresh cash
   evidence ($0 stops; at least 125 included minutes; maximum two hours old at
   gated steps). GitHub must supply the locked hosted image; otherwise STOP.
5. Andrew approves enablement and the fresh-seed ready-label tap. Then K-14 PASS
   precedes an approved second-repo canary, green KEYSTONE/#32 adoption/migration,
   and vendor cleanup. #32 remains draft.

Freeze SHA is the inactive candidate SHA. It is not deployed main's launch SHA:
main == GITHUB_SHA == K14_APPROVED_SHA must hold for an authorized live run, with
checker/approval evidence bound to that final revision. No merges, activation,
secret changes, issue/label launch tap or variable changes in this freeze.
