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
