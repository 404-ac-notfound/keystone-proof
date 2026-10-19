# K14 actual-run evidence checkpoint —19Oct17:16MYT
Author/collector: Magic. PARTIAL RUN EVIDENCE, not independent audit, final result or permission to change live code.
Actual run:39227996178 / https://github.com/404-ac-notfound/keystone-proof/actions/runs/39227996178
Retired skipped run:39227996208 (same label event; wrong ID in initial owner relay, corrected in PR13#6263753181).
Controller:6f1ce8c93454fc535d4158dea093a8f0d1169461; actual pilotPR14 headbe0d22f3ab3aeb04cf31e63b131b5a22f7a80978, base6f1ce8c. Patch only calc.py:return a-b -> return a+b (1 addition/1 deletion).
Launch/account receipt: PR13#6263748487, owner-relayed; no direct Magic settings inspection. One owner label setup event, subsequent controller writes observed. Full owner-touch accounting/duplicate/exhaust/stop audit still pending; no zero-touch acceptance invented.

## Direct observations
API job readback: guard, author, publish1, claim1 and request1 succeeded; verify1 polling in_progress. Actual guard/author/request logs show host ImageVersion20261012.334.1 admission before checkout; reviewed guard checks Python3.12.3. Author logs show locked CLI download/hash verification.
Author-runtime artifact12175311332 downloaded via GitHub artifact tool and its ZIP SHA256 verified as68dd0ef8f4262fa5c23103ed036c574e0ac63b7aa13ac1e86a87a3d048cc9187. Included actual-author-runtime.json is its parsed JSON, no tokens/secrets: CLI2.1.296/SHA25624972e3bc859fab2b46ed4c1e51f7d6130f06d3bd550811a114640de3370d0de; fresh session1ca5b5c3-9467-45c8-87de-14e935d984a2;4turns;reported usage retained. This usage object is not an independent billing invoice or credential-retirement proof.
Request6263736045 at09:11:10Z/17:11:10MYT, sender404-ac-notfound, exact single @codex review marker/head/base. Provider summary6263740675 completed09:12:27Z; provider clean receipt6263758228 at09:12:25Z. Actual manual provider response observed, not configuration-only inference. Standard review and inline endpoints were empty at capture.

## Newly discovered compatibility blocker
[Issue15](https://github.com/404-ac-notfound/keystone-proof/issues/15) records observed v1 summary/receipt format. Summary has exact40-character SHA in structured metadata, completed/no-findings fields, but no CLEAN prose; clean receipt uses only10-character reviewed SHA. Installed bind()/classify() replay on captured actual API bodies returns NO-VERDICT. Exact captured bodies, publisher/timestamps and raw UTF-8 hashes are preserved in live-response-sources.json; replay result in live-response-replay.json.
No bot response edited, prefix accepted, verdict forged, extra request issued or runtime code patched. Provider review completion is separate from controller acceptance. Current workflow has not reached finalcheck; no transportPASS or final tests claimed. Do not weaken an exact-head gate to rescue a run.

## Remaining external events/gates
Existing controller keeps its bounded wait/stop behavior. Facts age out at17:37:25MYT at gated steps; outer use stop18:00. Terminal/cancel/deadline triggers Jarvis's already-authorized issuer revocation/secret deletion and stop action with actual evidence. No rerun, new label, reset claim/attempt, live config replacement, extra smoke or new seed.
When terminal: collect all final jobs/artifacts/stop reason and exact final-head evidence; reconcile closure and obtain independent audit under existing gate. Access/runtime outcome staysBLOCKED. This live-format defect is new evidence not covered by mock/offline PASSes; later fix/relaunch requires separate scoped disposition and a fresh unused pilot/seed plus valid credentials. Do not reuse consumed identities.
This checkpoint preserves evidence while the real run is active; no background process/watch or completed audit is implied by publication.
