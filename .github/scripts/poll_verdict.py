#!/usr/bin/env python3
"""K-14 verdict poll. Reads the PR through the REST API (via the gh CLI),
waits for the pinned verifier's post that is bound to the expected head SHA,
and classifies it. Never infers approval from silence. Stdlib only."""
import json
import os
import re
import subprocess
import sys
import time

CLEAN_RE = re.compile(
    r"(did(?:n'?t| not)|didn.t)\s+find\s+any\s+(major\s+)?(issues|problems)"
    r"|no\s+major\s+(issues|problems)|no\s+issues\s+found|found\s+no\s+(major\s+)?issues",
    re.I,
)
HEX_RE = re.compile(r"\b[0-9a-f]{7,40}\b")


def names_sha(text, sha):
    return any(sha.startswith(t) for t in HEX_RE.findall((text or "").lower()))


def bind(kind, post, expected, other_heads):
    """Return bound_by or None. Posting time never binds."""
    body = post.get("body") or ""
    names_expected = names_sha(body, expected)
    names_other = any(names_sha(body, h) for h in other_heads if h)
    if kind == "review" and post.get("commit_id") == expected:
        # a post that names a different head as reviewed, without the expected one, is unbound
        return None if (names_other and not names_expected) else "commit_id"
    if kind == "review_comment" and post.get("original_commit_id") == expected:
        return None if (names_other and not names_expected) else "original_commit_id"
    if names_expected:
        return "reviewed_sha"
    return None


def classify(bound):
    """bound: list of dicts with kind, body. Returns REVIEW-CLEAN / REVIEW-WITH-FINDINGS / None."""
    substantive = [p for p in bound if (p.get("body") or "").strip()]
    if not substantive:
        return None  # empty reviews are NO-VERDICT by contract
    inline = [p for p in substantive if p["kind"] == "review_comment"]
    top = [p for p in substantive if p["kind"] != "review_comment"]
    if inline:
        return "REVIEW-WITH-FINDINGS"
    if top and all(CLEAN_RE.search(p["body"]) for p in top):
        return "REVIEW-CLEAN"
    return "REVIEW-WITH-FINDINGS"


def gh_json(path, paginate=True):
    cmd = ["gh", "api"] + (["--paginate", "--slurp"] if paginate else []) + [path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300])
    data = json.loads(r.stdout)
    if paginate:
        flat = []
        for page in data:
            flat.extend(page if isinstance(page, list) else [page])
        return flat
    return data


def author(post):
    u = post.get("user") or {}
    return u.get("login", ""), u.get("type", ""), post.get("author_association", "")


def collect(repo, pr):
    out = []
    for r in gh_json(f"repos/{repo}/pulls/{pr}/reviews?per_page=100"):
        if r.get("state") == "PENDING" or not r.get("submitted_at"):
            continue
        out.append(("review", r))
    for c in gh_json(f"repos/{repo}/pulls/{pr}/comments?per_page=100"):
        out.append(("review_comment", c))
    for c in gh_json(f"repos/{repo}/issues/{pr}/comments?per_page=100"):
        out.append(("issue_comment", c))
    return out


def main():
    repo = os.environ["GH_REPO"]
    pr = os.environ["PR"]
    expected = os.environ["EXPECTED"]
    verifier = os.environ["VERIFIER_LOGIN"]
    label = os.environ["LABEL"]
    minutes = float(os.environ.get("MINUTES", "30"))
    other_heads = [h for h in os.environ.get("OTHER_HEADS", "").split(",") if h]
    consumed_in = set()
    cpath = os.environ.get("CONSUMED_FILE", "")
    if cpath and os.path.exists(cpath):
        consumed_in = set(json.load(open(cpath)))
    started = time.time()
    deadline = started + minutes * 60
    first_bound_at = None
    reason = None
    head_moved = False
    seen_authors = {}
    raw = []
    bound = []
    while True:
        try:
            head = gh_json(f"repos/{repo}/pulls/{pr}", paginate=False)["head"]["sha"]
            if head != expected:
                head_moved = True
                reason = f"PR head moved to {head}"
                break
            posts = collect(repo, pr)
        except Exception as e:  # API trouble is logged, polling continues until the deadline
            print(f"poll error: {e}", flush=True)
            posts = []
        bound, raw = [], []
        for kind, p in posts:
            login, utype, assoc = author(p)
            if login == "github-actions[bot]":
                continue
            key = f"{kind}:{p['id']}"
            seen_authors[f"{login}|{utype}|{assoc}"] = True
            entry = {"id": key, "kind": kind, "login": login, "type": utype,
                     "association": assoc, "commit_id": p.get("commit_id"),
                     "original_commit_id": p.get("original_commit_id"),
                     "state": p.get("state"), "body": (p.get("body") or "")[:4000]}
            raw.append(entry)
            if login != verifier or key in consumed_in:
                continue
            b = bind(kind, p, expected, other_heads)
            if b:
                entry["bound_by"] = b
                bound.append(entry)
        if bound and first_bound_at is None:
            first_bound_at = time.time()
        now = time.time()
        if first_bound_at and now - first_bound_at >= 60:
            break
        if now >= deadline:
            break
        time.sleep(min(60, max(1, deadline - now)))
    try:
        checks = gh_json(f"repos/{repo}/commits/{expected}/check-runs?per_page=100", paginate=False)
        check_runs = [{"name": c.get("name"), "status": c.get("status"),
                       "conclusion": c.get("conclusion"),
                       "app": (c.get("app") or {}).get("slug")} for c in checks.get("check_runs", [])]
    except Exception as e:
        check_runs = [{"error": str(e)[:200]}]
    verdict = None if head_moved else classify(bound)
    if verdict is None:
        verdict = "NO-VERDICT"
        reason = reason or ("silence or unbound or empty output after "
                            f"{minutes:g} minutes" if not bound else "empty review")
    # first-seen diagnostics only; never scores
    first_seen = None
    for a in raw:
        if a["login"] not in ("claude[bot]",) and a["login"] != verifier:
            first_seen = a["login"]
            break
    consumed_out = sorted(consumed_in | {b["id"] for b in bound}) if verdict != "NO-VERDICT" else sorted(consumed_in)
    result = {
        "label": label, "pr": pr, "expected_head": expected, "verifier_login": verifier,
        "verdict": verdict, "reason": reason,
        "bound_by": sorted({b["bound_by"] for b in bound}) if verdict != "NO-VERDICT" else [],
        "consumed_ids": [b["id"] for b in bound] if verdict != "NO-VERDICT" else [],
        "quoted": [{"id": b["id"], "login": b["login"], "bound_by": b["bound_by"], "text": b["body"]} for b in bound],
        "observed_authors": sorted(seen_authors),
        "first_seen_actor_diagnostic": first_seen if verdict == "NO-VERDICT" else None,
        "check_runs": check_runs,
        "raw_observed": raw,
        "waited_seconds": int(time.time() - started),
    }
    os.makedirs("out", exist_ok=True)
    json.dump(result, open(f"out/verdict-{label}.json", "w"), indent=2)
    json.dump(consumed_out, open(f"out/consumed-{label}.json", "w"))
    with open(f"out/findings-{label}.md", "w") as f:
        f.write(f"# Verifier posts bound to {expected}\n\n")
        for q in result["quoted"]:
            f.write(f"## {q['id']} ({q['login']}, bound_by {q['bound_by']})\n\n{q['text']}\n\n")
    gout = os.environ.get("GITHUB_OUTPUT")
    if gout:
        with open(gout, "a") as f:
            f.write(f"verdict={verdict}\n")
            f.write(f"bound_by={','.join(result['bound_by'])}\n")
    print(json.dumps({k: result[k] for k in ("verdict", "reason", "bound_by", "observed_authors")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
