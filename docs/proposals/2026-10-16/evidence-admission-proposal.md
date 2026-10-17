# K-14 remaining evidence admission — concrete review proposal

Status: PROPOSED / NOT ADOPTED / NOT READY TO LAUNCH.
Prepared by Magic, 16 October 2026 MYT, after Andrew directed continued work.
Source base: keystone-proof main 9d1639983326670e96a1c07349ca653a906fcc76.
Only preparation documents change on this branch. No runtime/controller/workflow/lock changes.
Both existing final-main code PASSes remain attached to unchanged installed main.

## 1. Public runner capacity — source-backed resolution
GitHub documentation explicitly says standard GitHub-hosted runners are free and unlimited for public repositories:
https://docs.github.com/en/actions/reference/runners/github-hosted-runners
https://docs.github.com/en/billing/concepts/product-billing/github-actions

Magic freshly read repository metadata: private=false, visibility=public.
Every runs-on in installed k14-managed.yml is ubuntu-24.04, a documented standard public runner. The 13 job timeout caps sum to 117 minutes, within the existing 125-minute minimum reserve (117 <= 125). Preserve actual job timeouts unchanged. Factual correction after Urahara's review6229000429 of original proposal4cd3089; no evidence-admission policy or runtime change.

Disposition: the missing included-minute counter is NOT missing evidence of a private-plan balance for this public standard-runner route. Document capacity_basis=PUBLIC_STANDARD_RUNNER_FREE_UNLIMITED, provider source, current public-repo read and workflow SHA. A proposed K14_INCLUDED_MINUTES=125 denotes the existing bounded pilot reservation from that entitlement; it must NOT be described as a displayed remaining balance. This is a proposed source-backed interpretation of the existing minimum, not a change to runners or increased spend. Confirm this interpretation in the bounded evidence-admission review before setting variables. Scheduling/concurrency/image availability and storage are separate: free minutes do not guarantee a VM, unlimited storage, or bypass current $0 stops. If repo visibility or runner class changes, this basis stops applying.

## 2. Creation timestamps — conservative representation proposed
The real security predicate is maximum provider lifetime <=30 days and valid use ending before the conservative expiry bound. Exact seconds are unavailable in reported UI. Do not replace creation with notification time or secret updated_at.

PAT evidence: owner-session report token21163019 created15October; creation email notification2026-10-15T02:35:20Z; displayed expiry20October DATE. Proposed issuance interval:
- lower:2026-10-14T10:00:00Z (15October civil-day start at UTC+14, the earliest instant for that reported creation day across UTC-12..UTC+14).
- upper:2026-10-15T02:35:20Z (reported notification; not asserted exact issuance).
- expiry earliest:2026-10-19T10:00:00Z; expiry latest:2026-10-21T12:00:00Z.
- maximum lifetime measured from proposed issuance lower:170hours =7days2hours <30days.
The lower bound makes the lifetime test stricter than any issuance inside this interval. Upper<=now establishes existence before launch. Source is Jarvis-relayed provider/account evidence, not independent Magic email inspection. Reviewer must accept the creation-day evidence and interval before use.

Author OAuth: owner report of11October provisioning and16October UI "Connected5days ago". Proposed broad issuance interval from the reported11October civil day:
2026-10-10T10:00:00Z through2026-10-12T12:00:00Z.
No OAuth provider expiry is invented; keep expires_at=null and the existing OWNER_REVOCATION_BOUND. Review provenance/meaning of that coarse day evidence.

### Exact bounded decision required
Approve or reject this narrowly scoped encoding for THIS pilot:
- created_at is populated with accepted conservative issuance LOWER bound only;
- sibling evidence fields declare creation_precision=BOUNDED, creation_lower_bound, creation_upper_bound, creation_evidence, and that created_at is a conservative gate input, NOT actual provider issuance;
- validate ordered interval, upper<=launch-check time, lower<expiry-earliest, latest-expiry minus LOWER<=30days; retain interval evidence in the audit;
- preserve20October DATE expiry,19October10:00UTC launch/use stop,22October00:00UTC outer ceiling and terminal/cancel retirement.
The installed parser accepts only a timestamp and does not itself enforce these interval fields. Therefore this is an evidence-contract exception proposal requiring actual technical review and Andrew adoption; it is NOT silently compatible or already approved. Rejecting it means prepare a separately reviewed explicit bounds implementation, not ask Andrew to hunt unavailable seconds or mint another token.

## 3. Prepared values; still no ready envelope
See sibling evidence-inputs-proposed-20261016.json. It is an intentionally non-launchable preparation wrapper, not K14_PREFLIGHT_JSON. Pending authorizations/live evidence remain explicit. No generated passing envelope, synthetic completed evidence or variables have been produced.

Already settled:
PR8 merged; main9d16399 unchanged; both actual final-main receipts/hashes:
https://github.com/404-ac-notfound/keystone-proof/pull/8#issuecomment-6207831489
Owner accepted admin bypass and terminal/cancel/deadline retirement13:52MYT16Oct.
Old PAT revoked per account report.
Claude usage-credit switchOFF after reload17:30MYT, corrected report:
https://github.com/404-ac-notfound/keystone-proof/pull/8#issuecomment-6212516541
Preserve existing launchGO, seed7 and pilotK14-20261013-01.

## 4. Next work and genuine gates
Magic owns this concrete packet, bound arithmetic, final actual-preflight assembly and readback reconciliation.
Actual Urahara/accepted Claude reviewer: bounded evidence-interpretation review only; no repeat code review or source edits requested.
Andrew owns adoption of this explicit evidence-contract exception if supported by review. No repeated merge/admin-bypass/lifecycle/launchGO.
Authorized account/execution seat refreshes linked-user route/readiness and current $0/Codex/Claude state once this packet is resolved, near actual launch. Do not cycle fresh billing screenshots while unresolved preparation guarantees they expire.
Runtime/operator preserves pinned-image admission, exact finalmain/raw-comment readback, unused seed/claim checks, six prerequisite variables then enable last. No provider access from this cloud session assumed; actual review delivery remains unverified.

Validation: five pure expiry/bound arithmetic assertions run offline against selected installed request_expiry_bounds/utc/require/Stop definitions. Confirmed lower/upper dates,170hour maximum and exact allowed-use edge/+1s rejection predicate. This is arithmetic verification, not independent review, full gates() PASS, hosted image proof or live transport. No secrets inspected, no API/provider dispatch, no source merge or launch.
