# Approved installation revision — review handoff, 12 Oct 2026

Magic. Andrew explicitly instructed: “approve installation. and go ahead and push
the review ask of the installation.” This authorizes the installed copy and review
requests on draft PR #4 only. It is separate from the accidental UI approve draft,
which was invalidated/retracted. No PR merge, runtime switch, label or live launch.

## Exact change

- Add .github/workflows/k14-managed.yml, based on the previously reviewed disabled
  template. Rename to k14-managed, replace draft-only comments, remove needs: [].
- Guard and receipt job conditions now require vars.K14_ENABLED == 'true', so OFF
  or missing settings skip runner admission. Existing dependent jobs still require
  admitted guard/previous stages. No variable is set by this revision. Read-only GitHub Variables settings
  checked on 12 Oct during preparation: repository has no variables; K14_ENABLED
  is absent. No settings were modified.
- Pin request_login and launch_login to 404-ac-notfound in pure gates before any
  API call; avoid consuming a review slot for a mistyped posting identity.
- No permissions, environment names, secrets, provider/native/image hashes,
  dependency locks, review/revision/diff caps or timeout sums change. Legacy inert
  k14-pilot.yml retirement stub remains. The disabled template and unapplied patch
  remain historical preparation artifacts; installed workflow is the review target.
- Reconcile the project closure register against merged KEYSTONE PR #21 and its
  active supporting standard; checklist is the register's view. Overall K14 stays
  PARTIAL. New installed revision needs new review; old PASS is parent evidence.

## Independent review request — Kobe and Urahara

Inspect the exact PR #4 head SHA recorded in the PR body; stop if it changes.
Complete your first pass independently before reading the other new verdict.

Verify installed YAML syntax, job dependencies, OFF/missing job-level switch,
legacy retirement, unchanged permission/token boundaries/pins/caps and pure owner
identity gate. Exercise retained receipt, malformed preflight, comment/headline/
raw-body helper, final-main isolation and OAuth/window gates. Confirm the closure
register traces approved sources to implementation/review evidence and open
follow-ups without claiming a live PASS or K23 completion.

Author verification: 67 offline tests pass, including installed/template structural
comparison and wrong identity stops before API. Synthetic implementation evidence
only. Reviewers perform their own probes and read back head before posting one
verdict comment on PR #4. For PASS use exactly '<Seat>: PASS <full candidate SHA>'
as the first paragraph, then a blank line and scope/evidence. State candidate-only,
not final-main approval. Return the real comment URL/acknowledgement.

No commits, merges/closures, settings/permissions, secrets/variables, label events,
new workflows/provider pilot invocation or launch by reviewers. Review copy is
already installed on the draft branch; no reinstallation or activation action.

## After review

Andrew separately approves merge/legacy retirement if the installation reviews
pass. Both seats then recheck actual final main SHA; historical candidate comments
cannot be reused. Complete actual credential dates/use_until/retirement, fresh
readiness/cash/seed evidence and exact owner approval. K14_ENABLED stays OFF until
separate launch yes; set it last only after all other envelope values read back.

Full closure/follow-up state and next owners: closure-register.md. It is the only
K14 truth record; follow-up checklist below its register is a view. K23 proposal
R2 remains KEYSTONE draft PR #37; approved R1 is not silently superseded.
