# K-14 runner-lock refresh candidate — 17 October2026

Status: DRAFT / NOT ADOPTED / NOT INSTALLED. No provider/run/credential probe.
Base installed main9d1639983326670e96a1c07349ca653a906fcc76.

## Trigger and evidence
The17October readiness check found GitHub's current public Ubuntu24 image release20261012.334.1 at:
https://github.com/actions/runner-images/releases/tag/ubuntu24/20261012.334
Source commit7e7dc1bcc0ef464e5e315a2b4c33609590c6cffe:
https://github.com/actions/runner-images/blob/7e7dc1bcc0ef464e5e315a2b4c33609590c6cffe/images/ubuntu/Ubuntu2404-Readme.md
It documents Image Version20261012.334.1 and OS Python3.12.3. Installed workflow admits exact20261004.327.1 before checkout in all13 jobs. A VM on the newer release would stop, so current image readiness cannot be assumed.
A release publication does not prove a particular image is scheduled on the next job; only actual runtime admission proves that. No unapproved image probe is run.

## Minimal change
- All13 installed AND template ImageVersion checks/echoes refresh to20261012.334.1. Exact comparison stays fail-closed; no wildcard/multiple-image fallback.
- runtime-lock.json image_version and source_commit match that release.
- Python pin stays3.12.3, CLI stays2.1.296 with the same URL/SHA, dependency locks unchanged.
- Existing workflow assertion expects the reviewed new image, and existing changed-image test additionally rejects the old admitted image.
- Closure register records this material discovery and continued gates.
No controller logic, receipts, credentials, environments, permissions, actions, timeouts, budget, review counts, branch controls or live switches change.

## Validation
Author ran all77 existing unittest cases: PASS on local Linux Python3.12.14 / PyYAML6.0.3. These are local available dependencies, NOT a claim of the locked hosted image or hash-installed qa-requirements environment. Tests use synthetic/mocked binaries/APIs; "native binary verified" output is from that synthetic test, not a real Claude download.
The first local pass correctly caught13 old image expectations. Updated the existing literal assertion to new pin; corrected a local editing indentation error before publishing. Final77PASS. Old image is added to existing rejection test; no gate removed.
Static manifest/workflow/template comparison remains covered by the installation test.
No hosted scheduling, CLI download or real-token validity proof claimed.

## Review and adoption
Actual Urahara and owner-accepted Claude reviewer independently review exact candidate SHA and this source/diff. Bound the review to image/source pin and unchanged isolation/exhaust paths; do not restart resolved credential evidence debate or mislabel existing reviews. A candidatePASS is not actual-mainPASS.
Andrew separately approves any merge. After merge, both actual new-main receipts replace9d16399 receipts for launch; preserve old comments/history. Rebuild prepared preflight controller_sha/owner approval/raw hashes against actual resulting main, then fresh account readback and exact image admission; enable last under existing launchGO.
A draft branch does not authorize repinning live settings or consuming seed7/pilot. Existing seed7/pilotK14-20261013-01 and effective19October18:00MYT cutoff stay unchanged.
If current actual runner cannot meet the new exact image/CLI/Python pins, STOP; no silent repin/fallback/retry.
