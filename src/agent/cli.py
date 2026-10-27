import argparse
from pathlib import Path
from typing import Sequence

from src.agent.core import CodeReviewAgent
from src.llm.config import get_settings
from src.llm.gemini_api import GeminiApiClient


def run_cli(backend: str, argv: Sequence[str] | None = None) -> None:
    """Run a code review for a source file using the selected Gemini backend."""
    parser = argparse.ArgumentParser(description="Review a source file with Gemini.")
    parser.add_argument("file", type=Path, help="Path to the source file to review")
    args = parser.parse_args(argv)

    source_code = args.file.read_text(encoding="utf-8")
    settings = get_settings()
    if backend == "api":
        content_generator = GeminiApiClient(settings)
    elif backend == "sdk":
        from src.llm.google_genai import GoogleGenAIClient

        content_generator = GoogleGenAIClient(settings)
    else:
        raise ValueError(f"Unsupported Gemini backend: {backend}")

    try:
        result = CodeReviewAgent(content_generator).review(source_code)
    except RuntimeError as error:
        parser.exit(1, f"Error: {error}\n")
    print(result.model_dump_json(indent=2))
