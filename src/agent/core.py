from src.agent.prompts import SYSTEM_INSTRUCTION, build_review_prompt
from src.agent.state import ReviewResult
from src.llm.base import ContentGenerator


class CodeReviewAgent:
    """Generate and validate a structured code review using an LLM backend."""

    def __init__(self, content_generator: ContentGenerator) -> None:
        self._content_generator = content_generator

    def review(self, source_code: str) -> ReviewResult:
        """Review source code and validate the model response."""
        response = self._content_generator.generate(
            prompt=build_review_prompt(source_code),
            system_instruction=SYSTEM_INSTRUCTION,
        )
        return ReviewResult.model_validate_json(response)
