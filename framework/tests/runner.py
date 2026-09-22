"""Test orchestration and coverage analysis."""

import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


class TestRunner:
    """Orchestrate test discovery and execution."""

    def __init__(self, test_dir: str = "tests", parallel: bool = True):
        self.test_dir = Path(test_dir)
        self.parallel = parallel
        self.results: Dict[str, dict] = {}

    def discover_tests(self) -> List[Path]:
        """Discover test files."""
        if not self.test_dir.exists():
            logger.warning(f"Test directory not found: {self.test_dir}")
            return []

        test_files = []
        for pattern in ["test_*.py", "*_test.py"]:
            test_files.extend(self.test_dir.glob(pattern))

        logger.info(f"Discovered {len(test_files)} test files")
        return test_files

    def run_tests(self) -> Dict[str, dict]:
        """Run discovered tests."""
        test_files = self.discover_tests()
        if not test_files:
            logger.warning("No test files found")
            return {}

        for test_file in test_files:
            self._run_test_file(test_file)

        return self.results

    def _run_test_file(self, test_file: Path) -> None:
        """Run a single test file."""
        try:
            start_time = time.time()
            result = subprocess.run(
                ["python", "-m", "pytest", str(test_file), "-v"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            duration = time.time() - start_time

            self.results[str(test_file)] = {
                "status": "passed" if result.returncode == 0 else "failed",
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

            logger.info(f"Test {test_file}: {self.results[str(test_file)]['status']} ({duration:.2f}s)")
        except subprocess.TimeoutExpired:
            logger.error(f"Test {test_file} timed out")
            self.results[str(test_file)] = {
                "status": "timeout",
                "duration": 300,
                "error": "Test execution timed out",
            }
        except Exception as e:
            logger.error(f"Failed to run test {test_file}: {e}")
            self.results[str(test_file)] = {"status": "error", "error": str(e)}

    def get_summary(self) -> dict:
        """Get test execution summary."""
        if not self.results:
            return {"total": 0, "passed": 0, "failed": 0, "errors": 0}

        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r.get("status") == "passed")
        failed = sum(1 for r in self.results.values() if r.get("status") == "failed")
        errors = sum(1 for r in self.results.values() if r.get("status") == "error")

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
        }

    def export_results(self, filepath: str) -> None:
        """Export test results to JSON."""
        data = {"summary": self.get_summary(), "results": self.results}
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Test results exported to {filepath}")


class CoverageAnalyzer:
    """Analyze test coverage."""

    def __init__(self, source_dir: str = "src"):
        self.source_dir = Path(source_dir)
        self.coverage: Dict[str, float] = {}

    def analyze(self) -> Dict[str, float]:
        """Analyze code coverage."""
        try:
            result = subprocess.run(
                ["python", "-m", "coverage", "run", "-m", "pytest"],
                capture_output=True,
                text=True,
            )

            if result.returncode not in [0, 1]:
                logger.error(f"Coverage analysis failed: {result.stderr}")
                return {}

            report_result = subprocess.run(
                ["python", "-m", "coverage", "json"],
                capture_output=True,
                text=True,
            )

            if report_result.returncode == 0 and Path(".coverage.json").exists():
                with open(".coverage.json") as f:
                    coverage_data = json.load(f)
                    for file_path, file_coverage in coverage_data.get("files", {}).items():
                        if "summary" in file_coverage:
                            summary = file_coverage["summary"]
                            percent_covered = (
                                summary.get("percent_covered", 0) if summary else 0
                            )
                            self.coverage[file_path] = percent_covered

            return self.coverage
        except Exception as e:
            logger.error(f"Coverage analysis error: {e}")
            return {}

    def get_summary(self) -> dict:
        """Get coverage summary."""
        if not self.coverage:
            return {"total_coverage": 0, "files": 0}

        avg_coverage = sum(self.coverage.values()) / len(self.coverage)
        return {
            "total_coverage": avg_coverage,
            "files": len(self.coverage),
            "files_by_coverage": self.coverage,
        }
