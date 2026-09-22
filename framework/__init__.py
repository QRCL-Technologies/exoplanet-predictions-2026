"""Comprehensive framework for results, audits, tests, USPTO, and network monitoring."""

from .audits import Auditor, AuditFinding
from .local_models import LocalLLMClient, OllamaClient, MistralClient
from .network import NetworkMonitor, NetworkTopologyMapper
from .results import ResultsTracker, TestResult
from .tests import TestRunner, CoverageAnalyzer
from .uspto import USPTOClient, PatentPortfolioManager

__version__ = "1.0.0"
__all__ = [
    "Auditor",
    "AuditFinding",
    "LocalLLMClient",
    "OllamaClient",
    "MistralClient",
    "NetworkMonitor",
    "NetworkTopologyMapper",
    "ResultsTracker",
    "TestResult",
    "TestRunner",
    "CoverageAnalyzer",
    "USPTOClient",
    "PatentPortfolioManager",
]
