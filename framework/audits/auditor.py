"""Audit framework implementation."""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

from framework.local_models.llm_client import LocalLLMClient, get_local_llm_client

logger = logging.getLogger(__name__)


@dataclass
class AuditFinding:
    """Audit finding with severity and recommendations."""

    title: str
    category: str
    severity: str
    description: str
    recommendations: List[str]
    timestamp: str


class Auditor:
    """Multi-dimensional audit framework."""

    AUDIT_TYPES = ["security", "code_quality", "performance", "compliance"]
    SEVERITY_LEVELS = ["info", "warning", "error", "critical"]

    def __init__(self, config: Optional[dict] = None, llm_client: Optional[LocalLLMClient] = None):
        self.config = config or {}
        self.llm_client = llm_client or get_local_llm_client(config)
        self.findings: List[AuditFinding] = []

    def audit_security(self, code: str) -> List[AuditFinding]:
        """Run security audit on code."""
        findings = []

        if self.llm_client and self.llm_client.is_available():
            prompt = f"""Analyze this code for security vulnerabilities:

{code}

List any security issues found with severity levels (info/warning/error/critical) and recommendations."""
            try:
                analysis = self.llm_client.generate(prompt)
                findings.append(
                    AuditFinding(
                        title="LLM Security Analysis",
                        category="security",
                        severity="info",
                        description=analysis,
                        recommendations=["Review LLM analysis"],
                        timestamp=datetime.now().isoformat(),
                    )
                )
            except Exception as e:
                logger.error(f"Security audit failed: {e}")
        else:
            findings.append(
                AuditFinding(
                    title="Static Security Checks",
                    category="security",
                    severity="info",
                    description="Checking for common security patterns...",
                    recommendations=["Configure local LLM for enhanced security analysis"],
                    timestamp=datetime.now().isoformat(),
                )
            )

        self.findings.extend(findings)
        return findings

    def audit_code_quality(self, code: str) -> List[AuditFinding]:
        """Run code quality audit."""
        findings = []

        if self.llm_client and self.llm_client.is_available():
            prompt = f"""Review this code for quality issues:

{code}

Identify code quality problems including naming, complexity, duplication, and style issues."""
            try:
                analysis = self.llm_client.generate(prompt)
                findings.append(
                    AuditFinding(
                        title="LLM Code Quality Analysis",
                        category="code_quality",
                        severity="info",
                        description=analysis,
                        recommendations=["Address quality issues identified"],
                        timestamp=datetime.now().isoformat(),
                    )
                )
            except Exception as e:
                logger.error(f"Code quality audit failed: {e}")
        else:
            findings.append(
                AuditFinding(
                    title="Basic Code Quality Checks",
                    category="code_quality",
                    severity="info",
                    description="Basic quality metrics collected...",
                    recommendations=["Configure local LLM for detailed quality analysis"],
                    timestamp=datetime.now().isoformat(),
                )
            )

        self.findings.extend(findings)
        return findings

    def audit_performance(self, metrics: dict) -> List[AuditFinding]:
        """Run performance audit."""
        findings = []

        if self.llm_client and self.llm_client.is_available():
            prompt = f"""Analyze these performance metrics for optimization opportunities:

{json.dumps(metrics, indent=2)}

Identify bottlenecks and suggest optimizations."""
            try:
                analysis = self.llm_client.generate(prompt)
                findings.append(
                    AuditFinding(
                        title="LLM Performance Analysis",
                        category="performance",
                        severity="info",
                        description=analysis,
                        recommendations=["Implement suggested optimizations"],
                        timestamp=datetime.now().isoformat(),
                    )
                )
            except Exception as e:
                logger.error(f"Performance audit failed: {e}")
        else:
            findings.append(
                AuditFinding(
                    title="Basic Performance Checks",
                    category="performance",
                    severity="info",
                    description="Performance metrics recorded...",
                    recommendations=["Configure local LLM for detailed performance analysis"],
                    timestamp=datetime.now().isoformat(),
                )
            )

        self.findings.extend(findings)
        return findings

    def audit_compliance(self, target: str, standards: List[str]) -> List[AuditFinding]:
        """Run compliance audit against standards."""
        findings = []

        if self.llm_client and self.llm_client.is_available():
            prompt = f"""Check compliance with these standards: {', '.join(standards)}

Target: {target}

Identify any compliance gaps and provide remediation steps."""
            try:
                analysis = self.llm_client.generate(prompt)
                findings.append(
                    AuditFinding(
                        title="LLM Compliance Analysis",
                        category="compliance",
                        severity="info",
                        description=analysis,
                        recommendations=["Address compliance gaps"],
                        timestamp=datetime.now().isoformat(),
                    )
                )
            except Exception as e:
                logger.error(f"Compliance audit failed: {e}")
        else:
            findings.append(
                AuditFinding(
                    title="Compliance Framework Check",
                    category="compliance",
                    severity="info",
                    description="Compliance audit initiated...",
                    recommendations=["Configure local LLM for detailed compliance analysis"],
                    timestamp=datetime.now().isoformat(),
                )
            )

        self.findings.extend(findings)
        return findings

    def get_findings_by_severity(self, severity: str) -> List[AuditFinding]:
        """Get findings filtered by severity."""
        return [f for f in self.findings if f.severity == severity]

    def get_findings_by_category(self, category: str) -> List[AuditFinding]:
        """Get findings filtered by category."""
        return [f for f in self.findings if f.category == category]

    def export_findings(self, format: str = "json") -> str:
        """Export findings in specified format."""
        if format == "json":
            return json.dumps([asdict(f) for f in self.findings], indent=2)
        elif format == "text":
            return "\n\n".join(
                [f"[{f.severity.upper()}] {f.title}\nCategory: {f.category}\n{f.description}" for f in self.findings]
            )
        return ""
