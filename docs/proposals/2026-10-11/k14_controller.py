#!/usr/bin/env python3
"""Inactive K-14 controller candidate. Stdlib; external calls only in CLI modes.
Offline tests inject APIs. This is implementation validation, never an isolation check.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

REPO = "404-ac-notfound/keystone-proof"
VERIFIER = "chatgpt-codex-connector[bot]"
APPROVED_CONTROLLER_AUTHORS = frozenset({"Magic"})
REVIEW_PUBLISHER = "404-ac-notfound"
# Andrew's resumed pilot stops no later than 22 Oct; owner JSON cannot extend it.
PILOT_CEILING = "2026-10-22T00:00:00Z"
# Owner-approved exception: one-time, this K-14 pilot only, expires at the 19 Oct 18:00 MYT stop.
ADMISSION_PILOT = "K14-20261013-01"
ADMISSION_STOP = "2026-10-19T10:00:00Z"
PREFLIGHT_DEADLINE = "2026-10-19T08:00:00Z"
ADMISSION_DECISION = "https://github.com/404-ac-notfound/keystone-proof/pull/9#issuecomment-6259198586"
BASELINE_SHA = "1b7e33adcd4b25ba11328cc7070c3dcafec50e76"
BASELINE_REVIEWS = {
    "Urahara": (6246527351, "828e6dee231f813c637977a982379efb293a08e59a2bd3896b40d1e56b02e6d2"),
    "Kobe": (6246559739, "95bdefae681367e9da62d2559ee09b5007fd29001fa4e58efb615f0db4737809"),
}
ROOT = Path(__file__).resolve().parent
SHA = re.compile(r"^[0-9a-f]{40}$")
BODY_DIGEST = re.compile(r"^[0-9a-f]{64}$")
ISOLATION_COMMENT = re.compile(
    r"https://github\.com/404-ac-notfound/keystone-proof/(?:pull|issues)/([1-9][0-9]*)#issuecomment-([1-9][0-9]*)")
CLEAN = re.compile(r"no (?:major )?(?:issues|problems)(?: found)?|found no (?:major )?issues|did(?:n't| not) find any (?:major )?(?:issues|problems)", re.I)
FINDING = re.compile(r"\bP[0-3]\b|Codex Review:\s*Here are some suggestions", re.I)


class Stop(RuntimeError):
    pass


def require(condition, reason):
    if not condition:
        raise Stop(reason)


def utc(value):
    require(isinstance(value, str) and value.endswith("Z"), "missing/malformed UTC timestamp")
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise Stop("malformed UTC timestamp") from exc


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def request_expiry_bounds(credential):
    """Return use-validity lower bound and lifetime upper bound, not guessed expiry.

    Legacy exact timestamps remain supported. DATE evidence covers all civil
    timezones UTC-12..UTC+14; no timezone inference or provider header is trusted.
    """
    precision = credential.get("expiry_precision", "EXACT")
    require(precision in ("EXACT", "DATE"), "unknown request expiry precision")
    exact = credential.get("expires_at")
    date = credential.get("provider_expiry_date")
    require(credential.get("display_timezone") is None,
            "timezone-specific expiry admission unsupported")
    if precision == "EXACT":
        require(date is None, "exact expiry conflicts with provider date")
        expiry = utc(exact)
        return expiry, expiry
    require(exact is None and isinstance(date, str)
            and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date),
            "DATE expiry requires only a strict provider date")
    require(isinstance(credential.get("provider_expiry_evidence"), str)
            and credential["provider_expiry_evidence"].strip()
            and credential.get("validity_bound_basis") == "DATE_EARLIEST_INSTANT",
            "provider date evidence / validity-bound basis missing")
    try:
        midnight = dt.datetime.combine(dt.date.fromisoformat(date), dt.time(), dt.timezone.utc)
        earliest = midnight - dt.timedelta(hours=14)
        latest = midnight + dt.timedelta(days=1, hours=12)
    except (ValueError, OverflowError) as exc:
        raise Stop("invalid provider expiry date") from exc
    return earliest, latest


def validate_config_shape(c):
    """Reject malformed owner JSON before any dispatch, including receipt mode."""
    require(isinstance(c, dict), "preflight must be an object")
    for key in ("environment", "old_oauth_retirement", "author_credential", "request_credential"):
        require(isinstance(c.get(key), dict), key + " must be an object")
    require(c.get("owner_authorization") is None or isinstance(c["owner_authorization"], dict),
            "owner authorization must be an object")
    receipts = c.get("independent_isolation")
    require(isinstance(receipts, list) and all(isinstance(x, dict) for x in receipts),
            "isolation receipts must be a list of objects")
    require(all(isinstance(x.get("seat"), str) for x in receipts), "isolation seat must be a string")
    for key in ("author_credential", "request_credential"):
        for field in ("retirement", "protected_environment"):
            require(isinstance(c[key].get(field), dict), key + " " + field + " must be an object")
        if "revocation_bound" in c[key]:
            require(isinstance(c[key]["revocation_bound"], dict), key + " revocation bound must be an object")


def configuration_admission(c, expiry, now):
    """Configuration-only admission; unknown provider facts never become verified."""
    admission = c.get("configuration_admission")
    if admission is None:
        return False
    require(isinstance(admission, dict), "configuration admission must be an object")
    require(c.get("pilot_id") == ADMISSION_PILOT and c.get("seed_issue") == 7
            and c.get("repository") == REPO, "configuration admission is this pilot/repository only")
    require(admission.get("one_time") is True and admission.get("owner_decision") == ADMISSION_DECISION
            and admission.get("expires_at") == ADMISSION_STOP
            and now < expiry <= utc(ADMISSION_STOP), "configuration admission absent/expired/extended")
    require(c["environment"].get("status") == "UNKNOWN"
            and c.get("connected_user_access") == "UNKNOWN", "unexposed provider facts must stay UNKNOWN")
    for key in ("repo_review_configuration", "owner_app_installation_scope"):
        fact = admission.get(key)
        require(isinstance(fact, dict) and fact.get("status") == "CONFIGURATION_ONLY"
                and fact.get("evidence") and fact.get("repository") == REPO,
                "configuration-only admission evidence missing")
        checked = utc(fact.get("checked_at"))
        require(dt.timedelta(0) <= now - checked <= dt.timedelta(hours=2),
                "configuration admission evidence stale/future")
    install = admission["owner_app_installation_scope"]
    require(install.get("owner") == REVIEW_PUBLISHER and install.get("installation_id") == 161479376,
            "wrong owner/App installation scope")
    completed = utc(c.get("preflight_completed_at"))
    require(completed <= now and completed < utc(PREFLIGHT_DEADLINE),
            "preflight not green before 16:00 MYT; stand down")
    return True


def isolation_receipts(c, sha, admitted):
    """Keep exact baseline reviews; bind only the delta to the new launch SHA."""
    baseline = c.get("independent_isolation", [])
    if not admitted:
        return baseline, sha, []
    require(len(baseline) == 2 and {x.get("seat") for x in baseline} == set(BASELINE_REVIEWS),
            "exact baseline review pair missing")
    for r in baseline:
        comment_id, digest = BASELINE_REVIEWS[r["seat"]]
        require(r.get("status") == "PASS" and r.get("controller_sha") == BASELINE_SHA
                and r.get("comment_body_sha256") == digest
                and r.get("evidence") == f"https://github.com/{REPO}/pull/9#issuecomment-{comment_id}",
                "baseline review binding changed")
    delta = c.get("evidence_rule_delta_review")
    require(isinstance(delta, dict) and delta.get("seat") == "Kobe" and delta.get("status") == "PASS"
            and delta.get("controller_sha") == sha, "Kobe delta PASS required at final launch SHA")
    require(isinstance(delta.get("evidence"), str) and ISOLATION_COMMENT.fullmatch(delta["evidence"])
            and isinstance(delta.get("comment_body_sha256"), str)
            and BODY_DIGEST.fullmatch(delta["comment_body_sha256"]), "delta comment URL/body digest missing")
    return baseline, BASELINE_SHA, [delta]


def gates(c, e, now=None):
    """Validate pinned owner config and runtime variables. No provider or isolation probes."""
    validate_config_shape(c)
    now = now or now_utc()
    require(e.get("K14_ENABLED") == "true", "kill switch is OFF")
    require(e.get("GH_REPO") == REPO == c.get("repository"), "wrong repository")
    require(e.get("GITHUB_RUN_ATTEMPT") == "1", "rerun forbidden")
    require(c.get("request_login") == REVIEW_PUBLISHER and c.get("launch_login") == REVIEW_PUBLISHER,
            "request and launch identities must match the approved owner")
    sha = e.get("GITHUB_SHA", "")
    require(SHA.fullmatch(sha) and e.get("K14_APPROVED_SHA") == sha, "unapproved controller revision")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{2,80}", c.get("pilot_id", ""))
            and c["pilot_id"] != "UNASSIGNED", "pilot not assigned")
    expiry = utc(e.get("K14_EXPIRES_AT"))
    require(now < expiry <= utc(c.get("approved_expiry_ceiling")) <= utc(PILOT_CEILING),
            "expired or extended beyond approved envelope / 22 October ceiling")
    if c.get("pilot_id") == ADMISSION_PILOT:
        require(expiry <= utc(ADMISSION_STOP), "this pilot stops at 19 October 18:00 MYT")
        completed = utc(c.get("preflight_completed_at"))
        require(completed <= now and completed < utc(PREFLIGHT_DEADLINE),
                "preflight not green before 16:00 MYT; stand down")
    approval = c.get("owner_authorization") or {}
    require(approval.get("source") and approval.get("quote") and approval.get("approved_sha") == sha,
            "owner authorization absent or wrong revision")
    require(type(c.get("seed_issue")) is int and c["seed_issue"] > 1, "fresh seed issue not assigned")
    admitted = configuration_admission(c, expiry, now)
    require(admitted or (c.get("environment", {}).get("status") == "READY"
            and c["environment"].get("evidence")), "Codex environment readiness UNKNOWN/not ready")
    require((admitted or c.get("connected_user_access") == "VERIFIED")
            and c.get("managed_review_configuration") == "VERIFIED", "managed path access/configuration unverified")
    require(c.get("paid_review_credits") == "OFF_VERIFIED", "paid credit continuation unverified")
    retired = c.get("old_oauth_retirement", {})
    require(retired.get("secret_absence") == "VERIFIED" and retired.get("issuer_revocation") == "VERIFIED"
            and retired.get("evidence"), "old OAuth retirement unverified")
    require(c.get("max_reviews") == 2 and c.get("max_author_revisions") == 1
            and c.get("diff_caps") == {"files": 50, "changed_lines": 1000, "bytes": 131072}, "bounds differ from agreement")
    controller_author = c.get("controller_author")
    require(isinstance(controller_author, str) and controller_author in APPROVED_CONTROLLER_AUTHORS
            and approval.get("controller_author") == controller_author,
            "controller author must be identified, approved and bound to owner authorization")
    isolated, review_sha, _delta = isolation_receipts(c, sha, admitted)
    isolated = (len(isolated) == 2 and {x.get("seat") for x in isolated} == {"Urahara", "Kobe"}
                and all(x.get("status") == "PASS" and x.get("controller_sha") == review_sha
                        and x.get("seat") != c.get("controller_author") and x.get("evidence") for x in isolated))
    # Installation/merge produces the final launch SHA. Candidate checks cannot
    # substitute for both assigned checkers' receipts bound to that exact SHA.
    # KEYSTONE status supplies no alternative route through this hard gate.
    require(isolated, "Urahara/Kobe isolation PASS required at final approved launch SHA")
    for receipt in c["independent_isolation"]:
        evidence = receipt.get("evidence")
        digest = receipt.get("comment_body_sha256")
        require(isinstance(evidence, str) and ISOLATION_COMMENT.fullmatch(evidence)
                and isinstance(digest, str) and BODY_DIGEST.fullmatch(digest),
                "isolation evidence requires same-repo comment URL and exact body SHA-256")
    checked = utc(e.get("K14_CASH_CHECKED_AT"))
    require(dt.timedelta(0) <= now - checked <= dt.timedelta(hours=2), "cash evidence stale/future/missing")
    require(e.get("K14_CASH_STOP_VERIFIED") == "true" and e.get("K14_INCLUDED_MINUTES", "").isdigit()
            and int(e["K14_INCLUDED_MINUTES"]) >= 125, "$0 cash stops / 125-minute reserve unverified")
    for kind in ("author_credential", "request_credential"):
        credential = c.get(kind, {})
        issued = utc(credential.get("created_at"))
        if kind == "author_credential" and credential.get("revocation_bound"):
            require(utc(credential["revocation_bound"].get("revoke_by")) <= utc(PILOT_CEILING),
                    "author revocation bound exceeds 22 October ceiling")
        if kind == "author_credential" and credential.get("expires_at") is None:
            bound = credential.get("revocation_bound", {})
            require(bound.get("basis") == "OWNER_REVOCATION_BOUND"
                    and bound.get("owner") == c.get("launch_login") and bound.get("evidence"),
                    "author credential unknown expiry requires owner revocation bound")
            validity_bound = utc(bound.get("revoke_by"))
        elif kind == "request_credential":
            validity_bound, lifetime_bound = request_expiry_bounds(credential)
        else:
            validity_bound = utc(credential.get("expires_at"))
        use_until = utc(credential.get("use_until"))
        require(credential.get("evidence") and issued <= now < use_until <= expiry
                and use_until <= validity_bound,
                kind + " missing/expired/outside allowed-use window")
        retirement = credential.get("retirement", {})
        require(retirement.get("owner") == c.get("launch_login") and retirement.get("evidence")
                and retirement.get("on_terminal") is True and retirement.get("on_cancel") is True,
                kind + " terminal/cancel/use-until revoke-and-delete plan unverified")
        if kind == "request_credential":
            require(issued < validity_bound and
                    dt.timedelta(0) < lifetime_bound - issued <= dt.timedelta(days=30),
                    "request credential exceeds 30 days from issuance")
    require(c["author_credential"].get("fresh") is True, "fresh author OAuth not evidenced")
    for kind, name in (("author_credential", "k14-author-owner-approved"),
                       ("request_credential", "k14-review-owner-approved")):
        protected = c[kind].get("protected_environment", {})
        require(protected.get("name") == name and protected.get("status") == "VERIFIED"
                and protected.get("environment_only") is True and protected.get("evidence")
                and protected.get("deployment_branch") == "main"
                and protected.get("unattended_policy") == "VERIFIED",
                kind + " protected environment unavailable/unverified; no repository-secret fallback")
    return sha


def api(path, method="GET", payload=None, token=None, paginate=False, raw=False, page_key=None):
    env = os.environ.copy()
    env.pop("K14_REVIEW_REQUEST_TOKEN", None)
    if token:
        env["GH_TOKEN"] = token
    cmd = ["gh", "api", "--method", method]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    if raw:
        cmd += ["-H", "Accept: application/vnd.github.diff"]
    if payload is not None:
        cmd += ["--input", "-"]
    cmd += [path]
    result = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                            capture_output=True, text=True, timeout=45, env=env)
    # Do not copy stderr or request/secret material into evidence.
    require(result.returncode == 0, "GitHub API call failed; no automatic retry")
    if raw:
        return result.stdout
    data = json.loads(result.stdout)
    if not paginate:
        return data
    require(isinstance(data, list), "paginated API payload must be a page list")
    rows = []
    for page in data:
        if page_key is not None:
            require(isinstance(page, dict), "paginated API page must be an object")
            page = page.get(page_key)
        require(isinstance(page, list) and all(isinstance(x, dict) for x in page),
                "paginated API items must be objects in a list")
        rows.extend(page)
    return rows


def verify_isolation_comments(c, sha, get=None):
    admitted = c.get("configuration_admission") is not None
    baseline, review_sha, delta = isolation_receipts(c, sha, admitted)
    verified = verify_review_comments(baseline, review_sha, get)
    if delta:
        verified += verify_review_comments(delta, sha, get)
    return verified


def verify_review_comments(receipts, sha, get=None):
    """Read real pinned comments. Their publisher is owner-trusted, not a proof of seat independence."""
    get = get or api
    verified = []
    for receipt in receipts:
        link = ISOLATION_COMMENT.fullmatch(receipt["evidence"])
        require(link is not None, "invalid isolation comment URL")
        issue, comment_id = link.groups()
        comment = get(f"repos/{REPO}/issues/comments/{comment_id}")
        require(isinstance(comment, dict), "isolation comment payload must be an object")
        publisher = comment.get("user")
        require(isinstance(publisher, dict), "isolation comment user must be an object")
        require(type(comment.get("id")) is int and comment["id"] == int(comment_id)
                and comment.get("issue_url") == f"https://api.github.com/repos/{REPO}/issues/{issue}"
                and publisher.get("login") == REVIEW_PUBLISHER,
                "isolation comment identity/repository/publisher mismatch")
        body = comment.get("body")
        require(isinstance(body, str) and body.strip(), "isolation comment body missing")
        require(hashlib.sha256(body.encode("utf-8")).hexdigest() == receipt["comment_body_sha256"],
                "isolation comment changed or body digest mismatched")
        # Hash the exact API body above; normalise only the text used for parsing.
        # One canonical headline binds the verdict directly to its subject SHA.
        normalised = body.replace("\r\n", "\n")
        require("\r" not in normalised, "isolation comment has unsupported line endings")
        first_paragraph = normalised.split("\n\n", 1)[0]
        first_line = normalised.split("\n", 1)[0]
        require(first_paragraph == first_line, "isolation headline must be its own paragraph")
        seat = receipt["seat"]
        require(first_line == f"{seat}: PASS {sha}",
                "isolation comment must begin with canonical Seat: PASS full-approved-SHA")
        subjects = re.findall(r"(?<![0-9a-fA-F])[0-9a-fA-F]{40}(?![0-9a-fA-F])", first_paragraph)
        require(subjects and all(subject == sha for subject in subjects),
                "isolation comment opening paragraph contains another revision")
        verified.append({"seat": seat, "comment_id": int(comment_id), "controller_sha": sha,
                         "evidence": receipt["evidence"], "comment_body_sha256": receipt["comment_body_sha256"]})
    return verified


def emit(data, name):
    Path("out").mkdir(exist_ok=True)
    Path("out", name + ".json").write_text(json.dumps(data, indent=2) + "\n")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            for k, v in data.items():
                if isinstance(v, (str, int)) and "\n" not in str(v):
                    f.write(f"{k}={v}\n")


def current(c, pr, head=None, base=None, get=None):
    get = get or api
    require(str(pr).isdigit(), "PR missing")
    p = get(f"repos/{REPO}/pulls/{pr}")
    require(p.get("state") == "open" and p.get("head", {}).get("repo", {}).get("full_name") == REPO
            and p.get("base", {}).get("repo", {}).get("full_name") == REPO, "closed/fork/wrong repo PR")
    require(p["head"]["ref"] == f"job/{c['seed_issue']}" and p["base"]["ref"] == "main", "wrong pilot branch/base")
    require(SHA.fullmatch(p["head"]["sha"]) and SHA.fullmatch(p["base"]["sha"]), "invalid revision")
    require(not head or p["head"]["sha"] == head, "STALE: head moved")
    require(not base or p["base"]["sha"] == base, "STALE: base moved")
    return p


def caps(files, diff):
    require(0 < len(files) <= 50, "empty/oversized file set")
    require(sum(f["additions"] + f["deletions"] for f in files) <= 1000, "changed-line cap exceeded")
    require(len(diff.encode("utf-8")) <= 131072, "diff byte cap exceeded")
    require(all(f.get("patch") is not None for f in files), "binary/truncated/unsupported diff")


def reserve(c, look, pr, head, base, run_id, get=None):
    get = get or api
    require(look in (1, 2), "global two-review ceiling")
    p = current(c, pr, head, base, get)
    files = get(f"repos/{REPO}/pulls/{pr}/files?per_page=100", paginate=True)
    diff = get(f"repos/{REPO}/pulls/{pr}", raw=True)
    caps(files, diff)
    current(c, pr, head, base, get)
    # Atomic create-only ref consumes the slot before the request. Never update/delete it.
    ref = f"refs/heads/k14-attempts/{c['pilot_id']}/{look}"
    get(f"repos/{REPO}/git/refs", "POST", {"ref": ref, "sha": head})
    return {"look": look, "pr": str(pr), "head": head, "base": base, "run_id": str(run_id),
            "slot_ref": ref, "changed_files": len(files),
            "changed_lines": sum(f["additions"] + f["deletions"] for f in files),
            "diff_bytes": len(diff.encode("utf-8"))}


def request(c, claim, token, run_id, get=None):
    get = get or api
    require(bool(token), "request credential missing")
    require(claim["look"] in (1, 2) and claim["run_id"] == str(run_id), "invalid/cross-run claim")
    expected_ref = f"refs/heads/k14-attempts/{c['pilot_id']}/{claim['look']}"
    require(claim.get("slot_ref") == expected_ref, "wrong attempt reference")
    ref = get(f"repos/{REPO}/git/ref/heads/k14-attempts/{c['pilot_id']}/{claim['look']}")
    require(ref["object"]["sha"] == claim["head"], "claim revision mismatch")
    marker = f"<!-- k14-managed:{c['pilot_id']}:{claim['look']}:{claim['head']} -->"
    prior = get(f"repos/{REPO}/issues/{claim['pr']}/comments?per_page=100", paginate=True)
    require(not any(marker in (x.get("body") or "") for x in prior), "duplicate request; no resend")
    current(c, claim["pr"], claim["head"], claim["base"], get)
    # PAT used ONLY for this single comment creation. No checkout/model has this token.
    text = "@" + "codex review" + "\n\n" + marker + "\n"
    text += f"Review head {claim['head']} against base {claim['base']}. Review only; do not fix or push.\n"
    posted = get(f"repos/{REPO}/issues/{claim['pr']}/comments", "POST", {"body": text}, token=token)
    require(posted.get("user", {}).get("login") == c["request_login"], "wrong request posting identity; slot remains consumed")
    require(posted.get("id") and posted.get("created_at"), "request receipt incomplete; no resend")
    current(c, claim["pr"], claim["head"], claim["base"], get)
    return {**claim, "request_id": str(posted["id"]), "request_login": c["request_login"],
            "request_created_at": posted["created_at"], "request_url": posted.get("html_url")}


def bind(kind, post, head, request_time):
    # Versioned summary metadata has its own strict parser; never fall back to
    # finding a SHA or CLEAN phrase anywhere in an unsupported/malformed state.
    if kind == "issue" and "codex-review-state:" in (post.get("body") or ""):
        return None
    if post.get("user", {}).get("login") != VERIFIER:
        return None
    stamp = post.get("submitted_at") if kind == "review" else post.get("created_at")
    try:
        if utc(stamp) < utc(request_time):
            return None
    except Stop:
        return None
    if kind == "review" and post.get("state") in ("PENDING", "DISMISSED"):
        return None
    structured = post.get("commit_id") if kind == "review" else post.get("original_commit_id") if kind == "inline" else None
    if structured and structured != head:
        return None
    if structured == head:
        return "commit_id" if kind == "review" else "original_commit_id"
    # Full SHA only; timestamps, reactions and abbreviated SHAs never bind a verdict.
    return "full_reviewed_sha" if re.search(r"(?<![0-9a-f])" + head + r"(?![0-9a-f])", post.get("body") or "") else None


def managed_summary(post, req, now=None):
    """Parse the observed v1 issue-summary schema, within one request's PR/head.

    The provider exposes no request-id/base in this schema. Correlation rests on
    the same-PR endpoint, creation after our single request, exact full head,
    and current()'s unchanged base/head checks; it is not a provider request ACK.
    """
    body = post.get("body") or ""
    try:
        require(post.get("user", {}).get("login") == VERIFIER
                and post["user"].get("type") == "Bot"
                and post.get("performed_via_github_app", {}).get("id") == 1144995,
                "summary publisher mismatch")
        require(type(post.get("id")) is int and post["id"] > 0
                and post.get("issue_url") == f"https://api.github.com/repos/{REPO}/issues/{req['pr']}"
                and post.get("html_url") == f"https://github.com/{REPO}/pull/{req['pr']}#issuecomment-{post['id']}",
                "summary PR mismatch")
        require(SHA.fullmatch(req["head"]) and SHA.fullmatch(req["base"]), "invalid request SHAs")
        require(utc(req["request_created_at"]) <= utc(post.get("created_at"))
                <= utc(post.get("updated_at")) <= (now or now_utc()), "summary clock mismatch")
        require(body.startswith("<!-- codex-pull-request-review-summary -->\n")
                and body.count("codex-review-state:") == 1, "ambiguous summary marker")
        matches = re.findall(r"<!-- codex-review-state:v1 (\{[^\n]*\}) -->", body)
        require(len(matches) == 1, "unsupported summary state")

        def unique_keys(pairs):
            result = {}
            for key, value in pairs:
                require(key not in result, "duplicate summary key")
                result[key] = value
            return result

        state = json.loads(matches[0], object_pairs_hook=unique_keys)
        require(isinstance(state, dict) and set(state) == {"code_review", "security_review"},
                "unsupported summary root")
        review, security = state["code_review"], state["security_review"]
        keys = {"commit_sha", "has_any_findings", "has_unresolved_findings", "status"}
        require(isinstance(review, dict) and set(review) == keys
                and isinstance(security, dict) and set(security) == keys
                and all(value is None for value in security.values()), "unsupported review schema/scope")
        require(review["commit_sha"] == req["head"] and review["status"] == "completed"
                and type(review["has_any_findings"]) is bool
                and type(review["has_unresolved_findings"]) is bool
                and not (review["has_unresolved_findings"] and not review["has_any_findings"]),
                "incomplete/conflicting summary")
        # A findings flag alone supplies no actionable revision text. Bound
        # inline/prose findings still dominate classification when they arrive.
        return "NO-VERDICT" if review["has_any_findings"] else "REVIEW-CLEAN"
    except (Stop, ValueError, TypeError, KeyError, AttributeError):
        return "NO-VERDICT"


def review_record(kind, post, req, now=None):
    """Keep a versioned summary as a veto even when its state cannot be read."""
    versioned = kind == "issue" and "codex-review-state:" in (post.get("body") or "")
    if versioned:
        if post.get("user", {}).get("login") != VERIFIER:
            return None
        # Only records fetched from this request's PR endpoint reach this path.
        # An invalid bot summary blocks CLEAN, without borrowing another post.
        binding = "codex-review-state:v1"
    else:
        binding = bind(kind, post, req["head"], req["request_created_at"])
    if not binding:
        return None
    record = {"kind": kind, "id": post["id"], "login": VERIFIER,
              "body": post.get("body") or "", "state": post.get("state"),
              "bound_by": binding, "url": post.get("html_url")}
    if versioned:
        record["summary_verdict"] = managed_summary(post, req, now)
        if record["summary_verdict"] == "NO-VERDICT":
            record["bound_by"] = "unaccepted_summary_state"
    return record


def classify(posts):
    # A submitted change-request verdict is substantive even with no prose.
    if any(p.get("state") == "CHANGES_REQUESTED" for p in posts):
        return "REVIEW-WITH-FINDINGS"
    substantive = [p for p in posts if (p.get("body") or "").strip()]
    if any(p["kind"] == "inline" or FINDING.search(p["body"]) or p.get("state") == "CHANGES_REQUESTED" for p in substantive):
        return "REVIEW-WITH-FINDINGS"
    if substantive and all(p.get("summary_verdict") == "REVIEW-CLEAN"
                           if "summary_verdict" in p else CLEAN.search(p["body"])
                           for p in substantive):
        return "REVIEW-CLEAN"
    return "NO-VERDICT"


def actionable_findings(posts):
    """Revision input from bound findings only, never summary/status prose.

    Callers supply review_record() output, already bound to this request/head.
    A change-request state alone is a veto of CLEAN, not revision material.
    This checks the supported textual signals, not natural-language truth.
    """
    bodies = []
    for post in posts:
        body = (post.get("body") or "").strip()
        if (not body or "summary_verdict" in post
                or post.get("bound_by") in {"codex-review-state:v1", "unaccepted_summary_state"}
                or "codex-review-state:" in body):
            continue
        if not (post.get("kind") == "inline" or FINDING.search(body)
                or post.get("state") == "CHANGES_REQUESTED"):
            continue
        clean_text = CLEAN.search(body) or re.search(r"\bno (?:actionable )?findings\b", body, re.I)
        if clean_text and not FINDING.search(body):
            continue
        # Bare priority/header markers or a SHA alone are not actionable text.
        payload = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        payload = FINDING.sub("", payload)
        payload = CLEAN.sub("", payload)
        payload = re.sub(r"\bno (?:actionable )?findings\b", "", payload, flags=re.I)
        payload = re.sub(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", "", payload)
        if any(char.isalnum() for char in payload):
            bodies.append(body)
    return "\n\n".join(bodies)


def poll(c, req):
    deadline = time.monotonic() + 30 * 60
    result = {**req, "verifier_login": VERIFIER, "verdict": "NO-VERDICT", "reason": "timeout/unsupported response"}
    first_verdict = None
    last_snapshot = None
    while time.monotonic() < deadline:
        gates(c, os.environ)
        current(c, req["pr"], req["head"], req["base"])
        records = []
        for kind, path in (("review", f"pulls/{req['pr']}/reviews"),
                           ("inline", f"pulls/{req['pr']}/comments"),
                           ("issue", f"issues/{req['pr']}/comments")):
            for p in api(f"repos/{REPO}/{path}?per_page=100", paginate=True):
                record = review_record(kind, p, req)
                if record:
                    records.append(record)
        verdict = classify(records)
        if verdict == "REVIEW-WITH-FINDINGS" and not actionable_findings(records):
            # Keep polling for late inline/prose findings; never admit an
            # empty/summary-only revision or reinterpret the veto as CLEAN.
            verdict = "NO-VERDICT"
        snapshot = json.dumps(records, sort_keys=True)
        if verdict == "NO-VERDICT" or snapshot != last_snapshot:
            first_verdict = None
        last_snapshot = snapshot
        if verdict != "NO-VERDICT":
            if first_verdict is None:
                first_verdict = time.monotonic()
            # Allow inline findings to arrive after their parent review; re-read before accepting.
            if time.monotonic() - first_verdict >= 60:
                current(c, req["pr"], req["head"], req["base"])
                result.update(verdict=verdict, reason=None, posts=records, head_readback=req["head"], base_readback=req["base"])
                break
        time.sleep(min(30, max(0, deadline - time.monotonic())))
    result["checks"] = api(f"repos/{REPO}/commits/{req['head']}/check-runs?per_page=100")
    emit(result, "verdict")
    Path("out/findings.md").write_text(
        actionable_findings(result.get("posts", []))
        if result["verdict"] == "REVIEW-WITH-FINDINGS" else "")


def guard(c):
    sha = gates(c, os.environ)
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    require(event.get("action") == "labeled" and event.get("label", {}).get("name") == "ready"
            and event.get("sender", {}).get("login") == c["launch_login"]
            and event.get("issue", {}).get("number") == c["seed_issue"]
            and not event["issue"].get("pull_request"), "wrong launch event/seed/actor")
    # Both pure gates pass before read-only evidence calls; all comments verify
    # before the first claim write or any author/review provider invocation.
    verify_isolation_comments(c, sha)
    # This global pilot claim stops duplicate labels and new issues reusing the pilot id.
    api(f"repos/{REPO}/git/refs", "POST", {"ref": f"refs/heads/k14-claims/{c['pilot_id']}", "sha": sha})
    base = api(f"repos/{REPO}/git/ref/heads/main")["object"]["sha"]
    require(base == sha, "main moved since controller launch")
    api(f"repos/{REPO}/git/refs", "POST", {"ref": f"refs/heads/job/{c['seed_issue']}", "sha": base})
    emit({"admitted": "true", "base": base}, "guard")


def prepare(c, look):
    gates(c, os.environ)
    if look == 2:
        prior = json.loads(Path(".pilot/first/verdict.json").read_text())
        require(prior["verdict"] == "REVIEW-WITH-FINDINGS", "revision not admitted")
        findings = actionable_findings(prior.get("posts", []))
        require(bool(findings), "revision requires actionable bound findings")
        supplied = Path(".pilot/first/findings.md").read_text().strip()
        require(supplied == findings, "revision findings artifact mismatch")
        current(c, prior["pr"], prior["head"], prior["base"])
        blob = api(f"repos/{REPO}/contents/calc.py?ref={prior['head']}")
        import base64
        Path("calc.py").write_bytes(base64.b64decode(blob["content"]))
        Path(".pilot/findings.md").write_text(findings)


def finish_author(c, look):
    gates(c, os.environ)
    base = os.environ["BASE_SHA"]
    # Only calc.py goes to the branch. Scripts/config/tests from the author are never published.
    content = Path(".pilot/changed/calc.py").read_bytes()
    require(0 < len(content) <= 16384, "calc.py empty/oversized")
    require(subprocess.run(["git", "diff", "--quiet", "--", "test_calc.py"]).returncode == 0, "author changed test")
    branch = f"job/{c['seed_issue']}"
    branch_head = api(f"repos/{REPO}/git/ref/heads/{branch}")["object"]["sha"]
    pr = os.environ.get("PR")
    if look == 2:
        old = json.loads(Path(".pilot/first/verdict.json").read_text())
        require(branch_head == old["head"], "revision branch moved")
        current(c, pr, old["head"], base)
    else:
        require(branch_head == base, "author branch moved")
    original = api(f"repos/{REPO}/contents/calc.py?ref={branch_head}")
    import base64
    require(content != base64.b64decode(original["content"]), "author produced no change")
    commit = api(f"repos/{REPO}/contents/calc.py", "PUT", {
        "message": f"K-14 author look {look}: issue {c['seed_issue']}", "branch": branch,
        "sha": original["sha"], "content": base64.b64encode(content).decode("ascii")})
    head = commit["commit"]["sha"]
    if look == 1:
        # Open as a draft to avoid silently relying on managed automatic review on open.
        p = api(f"repos/{REPO}/pulls", "POST", {"title": f"K-14 bounded pilot {c['pilot_id']}",
            "head": branch, "base": "main", "draft": True,
            "body": f"Claude author; independent managed review requested in the same run. Refs #{c['seed_issue']}. No merge."})
        pr = p["number"]
    current(c, pr, head, base)
    emit({"pr": str(pr), "head": head, "base": base}, "author")


def finalcheck(c):
    gates(c, os.environ)
    current(c, os.environ["PR"], os.environ["HEAD_SHA"], os.environ["BASE_SHA"])
    import base64
    work = Path(os.environ["RUNNER_TEMP"]) / "verified-calculator"
    work.mkdir(exist_ok=True)
    for path, ref in (("calc.py", os.environ["HEAD_SHA"]), ("test_calc.py", os.environ["GITHUB_SHA"])):
        blob = api(f"repos/{REPO}/contents/{path}?ref={ref}")
        (work / path).write_bytes(base64.b64decode(blob["content"]))
    # No author OAuth or request PAT in this job; child receives no GitHub credentials.
    test_python = str(Path(os.environ["RUNNER_TEMP"]) / "k14-tests/bin/python")
    require(Path(test_python).is_file(), "hash-locked test venv missing")
    run = subprocess.run([test_python, "-m", "pytest", "-q", "test_calc.py"], cwd=work, capture_output=True,
                         text=True, timeout=60, env={"PATH": os.environ["PATH"], "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"})
    current(c, os.environ["PR"], os.environ["HEAD_SHA"], os.environ["BASE_SHA"])
    emit({"tests_green": "true" if run.returncode == 0 else "false", "head": os.environ["HEAD_SHA"],
          "base": os.environ["BASE_SHA"], "output": run.stdout[:8000]}, "tests")


def receipt(c):
    arts = Path("arts")
    records = {str(p.relative_to(arts)): json.loads(p.read_text()) for p in arts.rglob("*.json")}
    jobs = api(f"repos/{REPO}/actions/runs/{os.environ['GITHUB_RUN_ID']}/jobs?per_page=100", paginate=True, page_key="jobs")
    data = {"pilot_id": c["pilot_id"], "controller_sha": os.environ["GITHUB_SHA"], "environment": c["environment"],
            "connected_user_access": c.get("connected_user_access"),
            "configuration_admission": c.get("configuration_admission"),
            "preflight_completed_at": c.get("preflight_completed_at"),
            "evidence_rule_delta_review": c.get("evidence_rule_delta_review"),
            "records": records, "jobs": [{k: j.get(k) for k in ("id", "name", "started_at", "completed_at", "conclusion")}
                                        for j in jobs], "independent_isolation": c["independent_isolation"],
            "old_oauth_retirement": c["old_oauth_retirement"],
            "request_credential_validity": {key: c["request_credential"].get(key) for key in
                ("created_at", "expires_at", "expiry_precision", "provider_expiry_date",
                 "provider_expiry_evidence", "display_timezone", "validity_bound_basis", "use_until")},
            "owner_touches_after_launch": "UNKNOWN_PENDING_INDEPENDENT_AUDIT",
            "api_spend": "NO_API_PATH_INVOKED; billing evidence pending", "actions_minutes": "UNKNOWN_FINAL_USAGE_PENDING",
            "fresh_credential_retirement": "PENDING_OWNER_METADATA",
            "acceptance_scope": "K14_TRANSPORT_SUBTEST",
            "final_continuity_acceptance": {
                "spec_commit": "39e25bb6846a44ea56856d4f1b8af129401ac5f5",
                "spec_blob": "491bf56be82fa16e2fbbb6226bfdd1d77c678912",
                "outcome": "BLOCKED", "build_complete": False,
                "reason": "Kobe current-plan verification, Urahara method approval, Shaq image/QC, Git seat receipts and final-only image delivery not implemented",
                "alignment_record": "docs/proposals/2026-10-11/final-acceptance-alignment-20261012.md"},
            "outcome": "BLOCKED", "reason": "final usage, owner-touch audit and credential-retirement evidence pending"}
    # An artifact cannot magically verify billing or revocation. Never self-issue PASS.
    emit(data, "receipt")
    summary = "# K-14 receipt\n\n**Outcome: BLOCKED pending final evidence.**\n\n```json\n" + json.dumps(data, indent=2) + "\n```\n"
    Path("out/receipt.md").write_text(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(summary)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["guard", "prepare", "author", "reserve", "request", "poll", "finalcheck", "receipt"])
    parser.add_argument("--look", type=int, default=1)
    args = parser.parse_args()
    try:
        # Owner-provisioned non-secret JSON keeps approval/evidence out of a self-hash loop.
        # Default template is deliberately unlaunchable. The code revision is independently pinned.
        c = json.loads(os.environ.get("K14_PREFLIGHT_JSON") or (ROOT / "pilot-config.json").read_text())
        validate_config_shape(c)
        if args.mode not in {"guard", "receipt"}:
            verify_isolation_comments(c, gates(c, os.environ))
        if args.mode == "guard":
            guard(c)
        elif args.mode == "prepare":
            prepare(c, args.look)
        elif args.mode == "author":
            finish_author(c, args.look)
        elif args.mode == "reserve":
            gates(c, os.environ)
            emit(reserve(c, args.look, os.environ["PR"], os.environ["HEAD_SHA"], os.environ["BASE_SHA"],
                         os.environ["GITHUB_RUN_ID"]), "claim")
        elif args.mode == "request":
            gates(c, os.environ)
            claim = json.loads(Path(".pilot/claim/claim.json").read_text())
            emit(request(c, claim, os.environ.get("K14_REVIEW_REQUEST_TOKEN"), os.environ["GITHUB_RUN_ID"]), "request")
        elif args.mode == "poll":
            poll(c, json.loads(Path(".pilot/request/request.json").read_text()))
        elif args.mode == "finalcheck":
            finalcheck(c)
        else:
            receipt(c)
    except (Stop, KeyError, ValueError, TypeError, AttributeError, OSError, subprocess.TimeoutExpired) as exc:
        # No exception bodies: a library/process message could contain credential material.
        reason = str(exc) if isinstance(exc, Stop) else type(exc).__name__
        emit({"outcome": "BLOCKED", "reason": reason, "mode": args.mode}, "stop")
        print("BLOCKED:", reason)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

