"""Send a prompt to a local Ollama model.

Usage:
    python scripts/query_local_llm.py "Summarize cold-chain logistics."
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def ollama_base_url() -> str:
    """Return the Ollama OpenAI-compatible endpoint without duplicate /v1."""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    return base_url if base_url.endswith("/v1") else f"{base_url}/v1"


def ask_model(prompt: str) -> str:
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    client = OpenAI(
        base_url=ollama_base_url(),
        api_key="ollama",  # Ollama ignores this value; the SDK requires one.
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Query a local Ollama model")
    parser.add_argument("prompt", nargs="+", help="Prompt to send to the model")
    args = parser.parse_args()

    try:
        print(ask_model(" ".join(args.prompt)))
    except Exception as exc:
        raise SystemExit(
            "Could not reach the local Ollama model. Ensure `ollama serve` is running, "
            "the configured model is installed, and OLLAMA_BASE_URL is correct.\n"
            f"Details: {exc}"
        ) from exc


if __name__ == "__main__":
    main()
