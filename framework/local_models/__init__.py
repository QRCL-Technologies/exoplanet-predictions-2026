"""Local model integration for Ollama and Mistral."""

from .llm_client import LocalLLMClient, OllamaClient, MistralClient

__all__ = ["LocalLLMClient", "OllamaClient", "MistralClient"]
