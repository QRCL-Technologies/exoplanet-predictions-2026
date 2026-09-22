"""Test results tracking and export."""

import csv
import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Individual test result."""

    test_name: str
    status: str
    duration: float
    message: str
    timestamp: str


class ResultsTracker:
    """Track and export test results."""

    def __init__(self):
        self.results: List[TestResult] = []

    def add_result(self, test_name: str, status: str, duration: float, message: str = "") -> None:
        """Add a test result."""
        result = TestResult(
            test_name=test_name,
            status=status,
            duration=duration,
            message=message,
            timestamp=datetime.now().isoformat(),
        )
        self.results.append(result)
        logger.info(f"Test {test_name}: {status} ({duration:.2f}s)")

    def get_summary(self) -> dict:
        """Get summary statistics."""
        if not self.results:
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "total_duration": 0.0,
                "pass_rate": 0.0,
            }

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        skipped = sum(1 for r in self.results if r.status == "skipped")
        total_duration = sum(r.duration for r in self.results)
        pass_rate = (passed / (total - skipped)) * 100 if (total - skipped) > 0 else 0.0

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "total_duration": total_duration,
            "pass_rate": pass_rate,
        }

    def export_json(self, filepath: str) -> None:
        """Export results to JSON."""
        data = {
            "summary": self.get_summary(),
            "results": [asdict(r) for r in self.results],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Results exported to {filepath}")

    def export_csv(self, filepath: str) -> None:
        """Export results to CSV."""
        if not self.results:
            logger.warning("No results to export")
            return

        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["test_name", "status", "duration", "message", "timestamp"])
            writer.writeheader()
            for result in self.results:
                writer.writerow(asdict(result))
        logger.info(f"Results exported to {filepath}")

    def export_html(self, filepath: str) -> None:
        """Export results to HTML."""
        summary = self.get_summary()
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        .skipped {{ color: orange; }}
    </style>
</head>
<body>
    <h1>Test Results Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Tests: {summary['total']}</p>
        <p>Passed: {summary['passed']}</p>
        <p>Failed: {summary['failed']}</p>
        <p>Skipped: {summary['skipped']}</p>
        <p>Pass Rate: {summary['pass_rate']:.1f}%</p>
        <p>Total Duration: {summary['total_duration']:.2f}s</p>
    </div>
    <h2>Test Details</h2>
    <table>
        <tr>
            <th>Test Name</th>
            <th>Status</th>
            <th>Duration (s)</th>
            <th>Message</th>
            <th>Timestamp</th>
        </tr>
"""

        for result in self.results:
            status_class = result.status.lower()
            html += f"""        <tr>
            <td>{result.test_name}</td>
            <td class="{status_class}">{result.status}</td>
            <td>{result.duration:.2f}</td>
            <td>{result.message}</td>
            <td>{result.timestamp}</td>
        </tr>
"""

        html += """    </table>
</body>
</html>
"""

        with open(filepath, "w") as f:
            f.write(html)
        logger.info(f"Results exported to {filepath}")
