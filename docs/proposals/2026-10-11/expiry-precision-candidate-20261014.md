# K-14 conservative expiry admission — inactive candidate

Magic preparation under Andrew's 14 October KEYSTONE continuation. Installed
baseline stays f9ce391a7166e632d50c4c1145f75196e1d6d19a. No credential,
secret, variable, workflow definition, provider setting, claim, attempt or run
changed. Existing launch GO does not approve this changed installation.

Sources: [blocker](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6132513411)
and [design findings](https://github.com/404-ac-notfound/keystone-proof/pull/4#issuecomment-6132300091).
Andrew's resumed stop is no later than 2026-10-22T00:00:00Z. Enforce it
for the envelope, credential use windows and any author revocation bound.

## Contract

Legacy exact timestamps remain supported. Explicit expiry_precision EXACT
also works, with no provider date. Unknown precision stops. DATE requires:

- expires_at null; expiry_precision DATE;
- provider_expiry_date strictly YYYY-MM-DD and nonempty provider_expiry_evidence;
- display_timezone null/absent; validity_bound_basis DATE_EARLIEST_INSTANT.

Use the full civil timezone range UTC−12 through UTC+14. Timezone-specific
admission is unsupported. No credential/header probe and no guessed expiry.
For displayed date D, allowed use ends at D midnight UTC minus 14 hours;
the lifetime check uses D midnight UTC plus one day plus 12 hours. Issuance
must precede the lower bound; upper bound minus issuance must be positive
and at most 30 actual days. The offline envelope helper shares these gates.

**Existing token still fails:** creation 2026-10-11T13:35:58Z plus displayed
10 November gives lower 2026-11-09T10:00:00Z, upper 2026-11-11T12:00:00Z,
over 30 days. Shortening use_until does not prove provider lifetime.
Exact provider evidence remains the shortest route without needing DATE.
Otherwise Andrew provisions/enters a shorter-date replacement; recompute
from its actual issuance. Historical creation plus 9 November fits; this
example is neither replacement metadata nor rotation authority.

## Checks and gates

77 offline tests passed on local macOS Python 3.12 / PyYAML 6.0.2: 67 existing
plus ten expiry/ceiling tests. Synthetic evidence only, not hosted-runner,
isolation or transport proof. Covers current date rejected before API use,
exact regression, opposite bounds, malformed/conflicting dates, lifetime/use
edges, helper rejection, non-Z timestamps, leap/month/year boundaries and
non-overridable 22 October ceiling. Receipt captures non-secret validity
metadata for audit and still cannot self-issue PASS.

Required next sequence: independent Kobe/Urahara exact-candidate reviews;
Andrew's reviewed installation/merge approval; both actual final-main
rechecks with new SHA-bound receipts; complete real credential/retirement
metadata and fresh preflight; verify seed #7 / K14-20261013-01 unused;
build/read back prerequisite variables and enable last under approved scope;
one observed runtime receipt followed by independent audit and register closure.
The f9ce391 receipts cannot certify this changed controller. No widened scope,
cash/review/diff caps, verifier or isolation gate. K-23 remains incomplete.
