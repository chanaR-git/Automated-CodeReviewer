from typing import Protocol


class ContentGenerator(Protocol):
    def generate(self, prompt: str, system_instruction: str) -> str:
        """Generate text from a prompt and system instruction."""
