#!/usr/bin/env python3
"""K-14 receipt writer. Runs in the receipt job. Writes jobs/<issue>/receipt.md.
Failure receipt on any missing evidence. Designed clean-path skips are exempt."""
import json
import os
import pathlib

E = os.environ.get


def load(path):
    p = pathlib.Path(path)
    return json.loads(p.read_text()) if p.exists() else None


def main():
    issue = E("ISSUE")
    r_author, r_v1, r_rev, r_v2 = (E("RESULT_AUTHOR", ""), E("RESULT_VERIFY1", ""),
                                   E("RESULT_REVISE", ""), E("RESULT_VERIFY2", ""))
    verdict1, verdict2 = E("VERDICT1", ""), E("VERDICT2", "")
    head1, head2, pr = E("HEAD_1", ""), E("HEAD_2", ""), E("PR", "")
    pr_head_now = E("PR_HEAD_NOW", "")
    tests_green = E("VERIFIED_TESTS", "")  # "true" / "false" / "" (not run)
    v1 = load("arts/verdict-first/verdict-first.json")
    v2 = load("arts/verdict-second/verdict-second.json")
    ok_v = ("REVIEW-CLEAN", "REVIEW-WITH-FINDINGS")
    failures = []
    unexercised = []

    if r_author != "success":
        failures.append(f"author job result: {r_author or 'missing'}")
    else:
        if r_v1 != "success":
            failures.append(f"first look job result: {r_v1 or 'missing'}")
        elif verdict1 not in ok_v:
            failures.append(f"first look verdict: {verdict1 or 'missing'}")
        elif verdict1 == "REVIEW-CLEAN":
            # designed clean-path skips: revise and second look did not run, by design
            if r_rev == "skipped" and r_v2 == "skipped":
                unexercised = ["revise job", "second look"]
            else:
                failures.append(f"unexpected results after a clean first look: revise={r_rev}, verify2={r_v2}")
        else:  # findings
            if r_rev != "success":
                failures.append(f"revise job result: {r_rev or 'missing'}")
            elif r_v2 != "success":
                failures.append(f"second look job result: {r_v2 or 'missing'}")
            elif verdict2 not in ok_v:
                failures.append(f"second look verdict: {verdict2 or 'missing'}")

    revised = r_rev == "success" and r_v2 == "success" and verdict2 in ok_v
    verified_head = head2 if revised else head1
    if not verified_head:
        failures.append("no verified head recorded")
    elif pr_head_now != verified_head:
        failures.append(f"PR head now {pr_head_now or 'unreadable'} differs from verified head {verified_head}")
    if tests_green == "":
        failures.append("test result missing at the verified head")

    transport = "TRANSPORT FAIL" if failures else "TRANSPORT PASS (pending Andrew's billing read, kill criterion 6)"
    final_verdict = (verdict2 if revised else verdict1) or "none"
    task = f"tests green at verified head: {tests_green or 'not run'}; final verdict: {final_verdict}"

    L = []
    L.append(f"# K-14 pilot receipt, issue #{issue}\n")
    L.append(f"**TRANSPORT:** {transport}")
    L.append(f"**TASK:** {task}\n")
    if failures:
        L.append("## Failure reasons\n")
        L += [f"- {f}" for f in failures]
        L.append("")
    if unexercised:
        L.append(f"**UNEXERCISED (designed clean-path skip, not a failure):** {', '.join(unexercised)}\n")
    L.append("## Heads and ids\n")
    L.append(f"- PR: #{pr}")
    L.append(f"- head_1: `{head1}`")
    L.append(f"- head_2: `{head2 or 'none (no revision)'}`")
    L.append(f"- verified_head_sha: `{verified_head}`")
    L.append(f"- receipt_commit_sha: reported in the run job summary and the PR comment (a file cannot contain its own commit SHA)")
    L.append(f"- revise comment: id `{E('REVISE_COMMENT_ID','')}` created `{E('REVISE_COMMENT_AT','')}`")
    L.append(f"- run: {E('RUN_URL','')}\n")
    for name, v in (("First look", v1), ("Second look", v2)):
        L.append(f"## {name}\n")
        if not v:
            L.append("- not run, or no verdict file produced\n")
            continue
        L.append(f"- verdict: **{v['verdict']}** (reason: {v.get('reason')})")
        L.append(f"- verifier_identity (pinned login): `{v['verifier_login']}`")
        L.append(f"- bound_by: {', '.join(v['bound_by']) or 'n/a'}")
        L.append(f"- consumed ids: {', '.join(v['consumed_ids']) or 'none'}")
        L.append(f"- observed authors (login|type|association): {'; '.join(v['observed_authors']) or 'none'}")
        if v.get("first_seen_actor_diagnostic"):
            L.append(f"- first_seen_actor (diagnostic only, never scores): `{v['first_seen_actor_diagnostic']}`")
        L.append(f"- waited: {v['waited_seconds']} s")
        L.append(f"- check runs on the head: `{json.dumps(v['check_runs'])}`")
        for q in v["quoted"]:
            L.append(f"\n> verbatim from `{q['id']}` ({q['login']}):\n>\n" + "\n".join("> " + ln for ln in q["text"].splitlines()))
        if not v["quoted"]:
            L.append("\nRaw observed posts (NO-VERDICT evidence):\n")
            L.append("```json\n" + json.dumps(v["raw_observed"], indent=1)[:6000] + "\n```")
        L.append("")
    L.append("## Per-seat fields\n")
    L.append("| Seat | W-grade claimed | resume_mode | task pointer | waiting_for | resumed by | ack observed | completion |")
    L.append("|---|---|---|---|---|---|---|---|")
    L.append(f"| Claude Code Action | none: deterministic CI | EVENT-RESUMABLE per event, fresh each invocation | run {E('RUN_URL','')} | the `ready` label | label event (Andrew's tap) | author job {r_author or 'n/a'} | revise job {r_rev or 'n/a'} |")
    L.append(f"| Codex review | candidate W1-equivalent for this repo and event only, if a bound post exists | EVENT-RESUMABLE per PR event; thread targeting UNVERIFIED | PR #{pr} | PR-open (automatic review) | PR event; `@codex review` comment on revise path | first look: {verdict1 or 'n/a'} | second look: {verdict2 or 'n/a'} |")
    L.append("\nPilot scope note: a pass here says nothing about the quality of the code and does not move the KEYSTONE wake ledger.")
    out = pathlib.Path(f"jobs/{issue}/receipt.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n")
    print(transport)
    gout = E("GITHUB_OUTPUT")
    if gout:
        with open(gout, "a") as f:
            f.write(f"transport={'FAIL' if failures else 'PASS'}\n")


if __name__ == "__main__":
    main()
