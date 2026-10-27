import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.llm.config import Settings


class GeminiApiClient:
    """Call Gemini's generateContent REST endpoint using the standard library."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def generate(self, prompt: str, system_instruction: str) -> str:
        """Return generated text from the Gemini REST API."""
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._settings.model}:generateContent"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }
        request = Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self._settings.api_key,
            },
            method="POST",
        )

        try:
            with urlopen(
                request,
                timeout=self._settings.request_timeout_seconds,
            ) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            try:
                error_payload = json.loads(error.read().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                error_payload = {}
            error_details = error_payload.get("error", {})
            message = (
                error_details.get("message")
                if isinstance(error_details, dict)
                else None
            )
            raise RuntimeError(
                f"Gemini API request failed with HTTP {error.code}: "
                f"{message or error.reason}"
            ) from error
        except TimeoutError as error:
            raise RuntimeError(self._timeout_message()) from error
        except URLError as error:
            if isinstance(error.reason, TimeoutError):
                raise RuntimeError(self._timeout_message()) from error
            raise RuntimeError(
                f"Could not reach the Gemini API: {error.reason}"
            ) from error

        candidates = response_data.get("candidates", [])
        if not candidates:
            raise ValueError("Gemini API response did not contain any candidates.")

        parts = candidates[0].get("content", {}).get("parts", [])
        generated_text = "".join(
            part["text"] for part in parts if isinstance(part.get("text"), str)
        )
        if not generated_text:
            raise ValueError("Gemini API response did not contain generated text.")
        return generated_text

    def _timeout_message(self) -> str:
        return (
            "Gemini API request timed out after "
            f"{self._settings.request_timeout_seconds:g} seconds. "
            "Check your network connection, then increase "
            "GEMINI_REQUEST_TIMEOUT_SECONDS in .env if needed."
        )
