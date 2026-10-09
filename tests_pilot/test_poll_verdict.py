import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "pv", pathlib.Path(__file__).parent.parent / ".github/scripts/poll_verdict.py")
pv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pv)

H1 = "a" * 40
H2 = "b1c2d3e4f5" + "0" * 30


def test_review_binds_on_commit_id():
    assert pv.bind("review", {"commit_id": H1, "body": "x"}, H1, [H2]) == "commit_id"


def test_old_head_review_does_not_bind_to_new_head():
    assert pv.bind("review", {"commit_id": H1, "body": "x"}, H2, [H1]) is None


def test_inline_comment_uses_original_commit_id_not_commit_id():
    c = {"commit_id": H2, "original_commit_id": H1, "body": "bug here"}
    assert pv.bind("review_comment", c, H2, [H1]) is None
    assert pv.bind("review_comment", c, H1, [H2]) == "original_commit_id"


def test_issue_comment_needs_explicit_sha_prefix():
    assert pv.bind("issue_comment", {"body": "looks fine"}, H1, []) is None
    assert pv.bind("issue_comment", {"body": "Reviewed aaaaaaa ok"}, H1, []) == "reviewed_sha"
    assert pv.bind("issue_comment", {"body": "Reviewed aaaaaa ok"}, H1, []) is None  # 6 chars


def test_commit_bound_post_naming_other_head_is_unbound():
    body = f"Reviewed {H2[:8]}"
    assert pv.bind("review", {"commit_id": H1, "body": body}, H1, [H2]) is None


def test_classify():
    clean = {"kind": "review", "body": "Codex Review: Didn't find any major issues. Nice!"}
    assert pv.classify([clean]) == "REVIEW-CLEAN"
    findings = {"kind": "review", "body": "Codex Review: Here are some suggestions."}
    assert pv.classify([findings]) == "REVIEW-WITH-FINDINGS"
    assert pv.classify([clean, {"kind": "review_comment", "body": "P1 bug"}]) == "REVIEW-WITH-FINDINGS"
    assert pv.classify([{"kind": "review", "body": "  "}]) is None
    assert pv.classify([]) is None
