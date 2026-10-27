from google import genai
from google.genai import types

from src.llm.config import Settings


class GoogleGenAIClient:
    """Generate content through Google's official google-genai Python SDK."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = genai.Client(api_key=settings.api_key)

    def generate(self, prompt: str, system_instruction: str) -> str:
        """Return generated text from the Google GenAI SDK."""
        response = self._client.models.generate_content(
            model=self._settings.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            ),
        )
        if not response.text:
            raise ValueError("Google GenAI response did not contain generated text.")
        return response.text
