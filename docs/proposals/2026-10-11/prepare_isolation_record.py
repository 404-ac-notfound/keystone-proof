#!/usr/bin/env python3
"""Read one scoped GitHub review comment and prepare its exact raw-body hash; no writes."""
import argparse
import hashlib
import json

from k14_controller import api, require, SHA, ISOLATION_COMMENT, REPO, verify_isolation_comments


def prepare(url, seat, sha, get=None):
    require(isinstance(url, str) and ISOLATION_COMMENT.fullmatch(url), "same-repo isolation URL required")
    require(seat in ("Kobe", "Urahara") and isinstance(sha, str) and SHA.fullmatch(sha),
            "assigned seat and full approved revision required")
    comment_id = ISOLATION_COMMENT.fullmatch(url).group(2)
    comment = (get or api)(f"repos/{REPO}/issues/comments/{comment_id}")
    require(isinstance(comment, dict) and isinstance(comment.get("body"), str), "comment body must be text")
    record = {"seat": seat, "status": "PASS", "controller_sha": sha, "evidence": url,
              "comment_body_sha256": hashlib.sha256(comment["body"].encode("utf-8")).hexdigest()}
    verify_isolation_comments({"independent_isolation": [record]}, sha, lambda path: comment)
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--url", required=True)
    p.add_argument("--seat", choices=("Kobe", "Urahara"), required=True)
    p.add_argument("--sha", required=True)
    a = p.parse_args()
    print(json.dumps(prepare(a.url, a.seat, a.sha), indent=2))


if __name__ == "__main__":
    main()
