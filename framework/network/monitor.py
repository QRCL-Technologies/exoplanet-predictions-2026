"""Network monitoring and topology mapping."""

import json
import logging
import subprocess
import time
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class NetworkMonitor:
    """Monitor network health and connectivity."""

    def __init__(self, endpoints: Optional[List[str]] = None):
        self.endpoints = endpoints or []
        self.metrics: Dict[str, dict] = {}

    def add_endpoint(self, name: str, url: str) -> None:
        """Add an endpoint to monitor."""
        self.endpoints.append({"name": name, "url": url})
        logger.info(f"Added endpoint: {name} ({url})")

    def check_service_health(self, name: str, url: str, timeout: int = 5) -> dict:
        """Check health of a service."""
        start_time = time.time()
        try:
            response = requests.get(url, timeout=timeout)
            latency = (time.time() - start_time) * 1000

            health = {
                "name": name,
                "status": "healthy" if response.status_code == 200 else "degraded",
                "status_code": response.status_code,
                "latency_ms": latency,
                "timestamp": time.time(),
            }
        except requests.Timeout:
            health = {
                "name": name,
                "status": "timeout",
                "latency_ms": (time.time() - start_time) * 1000,
                "timestamp": time.time(),
            }
        except Exception as e:
            health = {
                "name": name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time(),
            }

        self.metrics[name] = health
        return health

    def monitor_connectivity(self, host: str = "8.8.8.8", count: int = 3) -> dict:
        """Monitor connectivity to a host."""
        try:
            result = subprocess.run(
                ["ping", "-c" if subprocess.os.name != "nt" else "-n", str(count), host],
                capture_output=True,
                text=True,
                timeout=30,
            )

            lines = result.stdout.split("\n")
            stats_line = [l for l in lines if "min/avg/max" in l or "Minimum" in l]

            if stats_line:
                return {
                    "host": host,
                    "status": "reachable",
                    "output": stats_line[0],
                }
            else:
                return {
                    "host": host,
                    "status": "unreachable",
                }
        except Exception as e:
            logger.error(f"Connectivity check failed: {e}")
            return {
                "host": host,
                "status": "error",
                "error": str(e),
            }

    def get_metrics(self) -> Dict[str, dict]:
        """Get all collected metrics."""
        return self.metrics

    def calculate_uptime(self, name: str, window_seconds: int = 3600) -> Optional[dict]:
        """Calculate uptime for a service."""
        if name not in self.metrics:
            return None

        metric = self.metrics[name]
        return {
            "service": name,
            "status": metric.get("status"),
            "last_check": metric.get("timestamp"),
            "window_seconds": window_seconds,
        }

    def export_metrics(self, filepath: str) -> None:
        """Export metrics to JSON."""
        with open(filepath, "w") as f:
            json.dump(self.metrics, f, indent=2, default=str)
        logger.info(f"Metrics exported to {filepath}")


class NetworkTopologyMapper:
    """Map and visualize network topology."""

    def __init__(self):
        self.topology: Dict[str, List[str]] = {}
        self.hosts: Dict[str, dict] = {}

    def add_host(self, name: str, address: str, role: str = "unknown") -> None:
        """Add a host to topology."""
        self.hosts[name] = {
            "address": address,
            "role": role,
            "connections": [],
        }
        logger.info(f"Added host: {name} ({address})")

    def add_connection(self, source: str, destination: str) -> None:
        """Add a connection between hosts."""
        if source not in self.topology:
            self.topology[source] = []
        self.topology[source].append(destination)
        logger.info(f"Added connection: {source} -> {destination}")

    def get_topology(self) -> Dict[str, dict]:
        """Get current topology."""
        return {
            "hosts": self.hosts,
            "connections": self.topology,
        }

    def export_topology(self, filepath: str, format: str = "json") -> None:
        """Export topology to file."""
        if format == "json":
            with open(filepath, "w") as f:
                json.dump(self.get_topology(), f, indent=2)
        elif format == "dot":
            with open(filepath, "w") as f:
                f.write("digraph Network {\n")
                for source, destinations in self.topology.items():
                    for dest in destinations:
                        f.write(f'  "{source}" -> "{dest}";\n')
                f.write("}\n")
        logger.info(f"Topology exported to {filepath}")

    def analyze_paths(self, source: str, destination: str) -> Optional[List[str]]:
        """Find path between two hosts (simple BFS)."""
        from collections import deque

        if source not in self.hosts or destination not in self.hosts:
            return None

        visited = set()
        queue = deque([(source, [source])])

        while queue:
            node, path = queue.popleft()
            if node == destination:
                return path

            if node in visited:
                continue
            visited.add(node)

            for neighbor in self.topology.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None
