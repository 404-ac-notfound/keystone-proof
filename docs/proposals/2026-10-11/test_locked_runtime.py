"""Offline bootstrap/credential validation; no model or isolation assessment."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("runtime", ROOT / "k14_runtime.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Bootstrap(unittest.TestCase):
    def download(self, data, expected):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"RUNNER_TEMP": d}), \
                patch.dict(m.LOCK["claude"], {"sha256": expected}), \
                patch.object(m.urllib.request, "urlopen", return_value=io.BytesIO(data)):
            path = Path(d) / "k14-claude"
            try:
                m.install_claude()
                self.assertEqual(path.read_bytes(), data)
                self.assertEqual(path.stat().st_mode & 0o777, 0o700)
            except RuntimeError:
                self.assertFalse(path.exists())
                raise

    def test_verified_download_becomes_executable(self):
        data = b"synthetic executable bytes"
        self.download(data, hashlib.sha256(data).hexdigest())

    def test_bad_hash_removes_download_and_never_executes(self):
        with patch.object(m.subprocess, "run") as run, self.assertRaisesRegex(RuntimeError, "SHA-256 mismatch"):
            self.download(b"tampered", "0" * 64)
        run.assert_not_called()

    def test_no_overwrite_or_redownload_of_preexisting_binary(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"RUNNER_TEMP": d}), \
                patch.object(m.urllib.request, "urlopen") as download:
            (Path(d) / "k14-claude").write_bytes(b"unexpected")
            with self.assertRaisesRegex(RuntimeError, "pre-existing"):
                m.install_claude()
            download.assert_not_called()

    def test_install_tests_rejects_different_python_before_any_install(self):
        with patch.object(m.subprocess, "check_output", return_value="Python 3.14.0\n"), \
                patch.object(m.subprocess, "run") as install, self.assertRaisesRegex(RuntimeError, "Python"):
            m.install_tests()
        install.assert_not_called()

    def test_test_install_starts_empty_and_requires_hashes(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {"RUNNER_TEMP": d}), \
                patch.object(m.subprocess, "check_output", return_value="Python 3.12.3\n"), \
                patch.object(m.subprocess, "run") as run:
            m.install_tests()
            commands = [call.args[0] for call in run.call_args_list]
            self.assertIn("venv", commands[0])
            for option in ("--require-hashes", "--only-binary=:all:", "--no-deps", "--no-cache-dir"):
                self.assertIn(option, commands[1])
            (Path(d) / "k14-tests").mkdir()
            with self.assertRaisesRegex(RuntimeError, "empty"):
                m.install_tests()

    def test_native_author_receives_only_author_credential_and_bounded_tools(self):
        with tempfile.TemporaryDirectory() as d:
            data = b"synthetic binary"
            (Path(d) / "k14-claude").write_bytes(data)
            env = {"RUNNER_TEMP": d, "CLAUDE_CODE_OAUTH_TOKEN": "synthetic OAuth",
                   "K14_REVIEW_REQUEST_TOKEN": "synthetic PAT", "GH_TOKEN": "synthetic GitHub",
                   "ANTHROPIC_API_KEY": "synthetic API", "ANTHROPIC_BASE_URL": "https://bad.invalid"}
            result = subprocess.CompletedProcess([], 0, json.dumps({"is_error": False, "session_id": "synthetic", "num_turns": 1}), "")
            old = os.getcwd()
            try:
                os.chdir(d)
                with patch.dict(os.environ, env), patch.dict(m.LOCK["claude"], {"sha256": hashlib.sha256(data).hexdigest()}), \
                        patch.object(m.subprocess, "run", return_value=result) as run:
                    m.author(1)
                    kwargs = run.call_args.kwargs
                    for key in ("K14_REVIEW_REQUEST_TOKEN", "GH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL"):
                        self.assertNotIn(key, kwargs["env"])
                    self.assertEqual(kwargs["env"]["DISABLE_AUTOUPDATER"], "1")
                    command = run.call_args.args[0]
                    for arg in ("--safe-mode", "--strict-mcp-config", "--no-session-persistence", "Read,Edit", "12"):
                        self.assertIn(arg, command)
                    self.assertNotIn("Bash", command)
                    self.assertNotIn("synthetic OAuth", Path("out/author-runtime.json").read_text())
            finally:
                os.chdir(old)

    def test_changed_image_stops_before_checkout(self):
        jobs = yaml.load((ROOT / "k14-managed.yml.disabled").read_text(), Loader=yaml.BaseLoader)["jobs"]
        for version in ("", "20261004.327.1", "20261011.999.1"):
            result = subprocess.run(["bash", "-c", jobs["guard"]["steps"][0]["run"]],
                                    env={**os.environ, "ImageOS": "ubuntu24", "ImageVersion": version}, capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

