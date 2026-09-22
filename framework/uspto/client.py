"""USPTO patent database client."""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class USPTOClient:
    """Client for USPTO patent database API."""

    BASE_URL = "https://developer.uspto.gov/ibd-api/v1"

    def __init__(self, api_key: Optional[str] = None, timeout: int = 30):
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {"Accept": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        self.cache: Dict[str, dict] = {}

    def search_patents(self, query: str, limit: int = 100) -> List[dict]:
        """Search for patents by keyword."""
        cache_key = f"search:{query}:{limit}"
        if cache_key in self.cache:
            logger.info(f"Using cached results for query: {query}")
            return self.cache[cache_key]

        try:
            url = f"{self.BASE_URL}/patent/search"
            params = {"q": query, "rows": min(limit, 1000)}

            response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            results = response.json().get("patents", [])
            self.cache[cache_key] = results
            logger.info(f"Found {len(results)} patents matching '{query}'")
            return results
        except Exception as e:
            logger.error(f"Patent search failed: {e}")
            return []

    def get_patent_details(self, patent_id: str) -> Optional[dict]:
        """Get detailed information about a patent."""
        cache_key = f"details:{patent_id}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            url = f"{self.BASE_URL}/patent/{patent_id}"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()

            patent_data = response.json()
            self.cache[cache_key] = patent_data
            logger.info(f"Retrieved details for patent {patent_id}")
            return patent_data
        except Exception as e:
            logger.error(f"Failed to get patent details: {e}")
            return None

    def search_by_inventor(self, inventor_name: str, limit: int = 100) -> List[dict]:
        """Search patents by inventor name."""
        query = f"inventor_name:{inventor_name}"
        return self.search_patents(query, limit)

    def search_by_assignee(self, assignee_name: str, limit: int = 100) -> List[dict]:
        """Search patents by assignee."""
        query = f"assignee_name:{assignee_name}"
        return self.search_patents(query, limit)

    def search_by_classification(self, classification: str, limit: int = 100) -> List[dict]:
        """Search patents by CPC classification."""
        query = f"cpc_class:{classification}"
        return self.search_patents(query, limit)

    def clear_cache(self) -> None:
        """Clear the result cache."""
        self.cache.clear()
        logger.info("Patent cache cleared")


class PatentPortfolioManager:
    """Manage a portfolio of patents."""

    def __init__(self, client: USPTOClient):
        self.client = client
        self.portfolio: List[dict] = []

    def add_patent(self, patent_id: str) -> bool:
        """Add a patent to portfolio."""
        details = self.client.get_patent_details(patent_id)
        if details:
            self.portfolio.append({
                "patent_id": patent_id,
                "details": details,
                "added_date": datetime.now().isoformat(),
            })
            logger.info(f"Added patent {patent_id} to portfolio")
            return True
        return False

    def search_and_add(self, query: str) -> int:
        """Search for patents and add results to portfolio."""
        results = self.client.search_patents(query)
        added_count = 0

        for result in results:
            patent_id = result.get("id") or result.get("patent_number")
            if patent_id and self.add_patent(patent_id):
                added_count += 1

        logger.info(f"Added {added_count} patents from search query")
        return added_count

    def get_portfolio_summary(self) -> dict:
        """Get summary of portfolio."""
        return {
            "total_patents": len(self.portfolio),
            "portfolio_value": "TBD",
            "coverage": "TBD",
            "patents": [
                {
                    "id": p["patent_id"],
                    "added_date": p["added_date"],
                } for p in self.portfolio
            ],
        }

    def export_portfolio(self, filepath: str) -> None:
        """Export portfolio to JSON."""
        with open(filepath, "w") as f:
            json.dump(self.get_portfolio_summary(), f, indent=2)
        logger.info(f"Portfolio exported to {filepath}")

    def get_filing_status(self, patent_id: str) -> Optional[dict]:
        """Get filing status of a patent."""
        details = self.client.get_patent_details(patent_id)
        if details:
            return {
                "patent_id": patent_id,
                "filing_date": details.get("filing_date"),
                "publication_date": details.get("publication_date"),
                "issue_date": details.get("issue_date"),
                "status": details.get("status", "unknown"),
            }
        return None
