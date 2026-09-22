"""Local LLM client for Ollama and Mistral."""

import logging
from abc import ABC, abstractmethod
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class LocalLLMClient(ABC):
    """Abstract base class for local LLM clients."""

    def __init__(self, endpoint: str, model: str, timeout: int = 30):
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text from prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if model is available."""
        pass


class OllamaClient(LocalLLMClient):
    """Ollama local model client."""

    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "mistral", timeout: int = 30):
        super().__init__(endpoint, model, timeout)
        self.api_url = f"{endpoint}/api/generate"

    def is_available(self) -> bool:
        """Check if Ollama server is available."""
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Ollama."""
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return ""


class MistralClient(LocalLLMClient):
    """Mistral local model client."""

    def __init__(
        self,
        endpoint: str = "http://localhost:8000",
        model: str = "mistral-7b",
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        super().__init__(endpoint, model, timeout)
        self.api_url = f"{endpoint}/v1/completions"
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def is_available(self) -> bool:
        """Check if Mistral server is available."""
        try:
            response = requests.get(f"{self.endpoint}/health", timeout=5, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Mistral not available: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Mistral."""
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": 1024,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("text", "").strip()
            return ""
        except Exception as e:
            logger.error(f"Mistral generation failed: {e}")
            return ""


def get_local_llm_client(config: dict) -> Optional[LocalLLMClient]:
    """Get configured local LLM client."""
    llm_type = config.get("local_models", {}).get("type", "ollama").lower()
    endpoint = config.get("local_models", {}).get("endpoint", "")

    if llm_type == "ollama":
        model = config.get("local_models", {}).get("model", "mistral")
        return OllamaClient(endpoint or "http://localhost:11434", model)
    elif llm_type == "mistral":
        model = config.get("local_models", {}).get("model", "mistral-7b")
        api_key = config.get("local_models", {}).get("api_key")
        return MistralClient(endpoint or "http://localhost:8000", model, api_key)

    return None
