"""Exercise report validation without GitHub access or real credentials."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


class ReportContainmentTests(unittest.TestCase):
    """Check partial downloads, symlinks, oversized reports, and PR injection."""

    def test_python_path_is_set_only_for_supported_interpreters(self) -> None:
        """Let the inline-comment action provision Python when the runner is too old."""
        action = Path(__file__).parents[1] / "action.yaml"
        scripts = re.findall(r"^      run: \|\n((?:        .*\n|\n)+)", action.read_text(), re.M)
        script = textwrap.dedent(scripts[0])
        for exit_code, expected_python in [("0", True), ("1", False)]:
            with (
                self.subTest(exit_code=exit_code),
                tempfile.TemporaryDirectory(prefix="python-path-test-") as tmp,
            ):
                root = Path(tmp)
                python = root / "python3"
                python.write_text(f"#!/bin/sh\nexit {exit_code}\n")
                python.chmod(0o755)
                output = root / "outputs"
                result = subprocess.run(
                    ["bash", "-e", "-c", script],
                    capture_output=True,
                    text=True,
                    env={
                        "PATH": f"{tmp}:{os.environ['PATH']}",
                        "RUNNER_TEMP": tmp,
                        "GITHUB_OUTPUT": str(output),
                    },
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                expected = f"python={python if expected_python else ''}\n"
                self.assertIn(expected, output.read_text())

    def test_validation(self) -> None:
        """Run the shipped validation program with isolated artifact fixtures."""
        action = Path(__file__).parents[1] / "action.yaml"
        scripts = re.findall(r"^      run: \|\n((?:        .*\n|\n)+)", action.read_text(), re.M)
        script = textwrap.dedent(scripts[1])
        for kind in ["normal", "symlink", "oversized", "invalid-pr", "failed-download"]:
            with (
                self.subTest(kind=kind),
                tempfile.TemporaryDirectory(prefix="report-test-") as tmp,
            ):
                root = Path(tmp)
                report = root / "clang-tidy-fixes.yaml"
                if kind == "symlink":
                    report.symlink_to(root / "outside")
                else:
                    report.write_text("x" * (2_000_001 if kind == "oversized" else 1))
                output = root / "outputs"
                result = subprocess.run(
                    ["bash", "-e", "-c", script],
                    capture_output=True,
                    text=True,
                    env={
                        "PATH": os.environ["PATH"],
                        "HOME": tmp,
                        "GITHUB_OUTPUT": str(output),
                        "INPUT_BUILD_PATH": tmp,
                        "DOWNLOAD_OUTCOME": "failure" if kind == "failed-download" else "success",
                        "INPUT_PR_NUMBER": "1\nspoof=true" if kind == "invalid-pr" else "1",
                    },
                )
                if kind in {"symlink", "oversized", "invalid-pr"}:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(output.exists())
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    expected = "false" if kind == "failed-download" else "true"
                    self.assertIn(f"has_fixes={expected}\n", output.read_text())


if __name__ == "__main__":
    unittest.main()
