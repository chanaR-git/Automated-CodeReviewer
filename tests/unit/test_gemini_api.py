import json
import unittest
from io import BytesIO
from urllib.error import HTTPError
from unittest.mock import MagicMock, patch

from src.llm.config import Settings
from src.llm.gemini_api import GeminiApiClient


class FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self) -> bytes:
        return self._payload


class GeminiApiClientTests(unittest.TestCase):
    @patch("src.llm.gemini_api.urlopen")
    def test_generate_posts_request_and_returns_text(
        self,
        mock_urlopen: MagicMock,
    ) -> None:
        mock_urlopen.return_value = FakeResponse(
            {"candidates": [{"content": {"parts": [{"text": '{"summary":"Clean"}'}]}}]}
        )
        client = GeminiApiClient(Settings(api_key="test-key"))

        result = client.generate("review this", "reviewer")

        self.assertEqual(result, '{"summary":"Clean"}')
        request = mock_urlopen.call_args.args[0]
        self.assertNotIn("test-key", request.full_url)
        self.assertEqual(request.get_header("X-goog-api-key"), "test-key")
        self.assertEqual(
            json.loads(request.data)["contents"][0]["parts"][0]["text"], "review this"
        )

    @patch("src.llm.gemini_api.urlopen")
    def test_generate_includes_api_error_message(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = HTTPError(
            "https://example.test",
            404,
            "Not Found",
            None,
            BytesIO(b'{"error":{"message":"The requested model was not found."}}'),
        )
        client = GeminiApiClient(Settings(api_key="test-key"))

        with self.assertRaisesRegex(
            RuntimeError,
            "HTTP 404: The requested model was not found.",
        ):
            client.generate("review this", "reviewer")

    @patch("src.llm.gemini_api.urlopen")
    def test_generate_explains_request_timeout(self, mock_urlopen: MagicMock) -> None:
        mock_urlopen.side_effect = TimeoutError("read timed out")
        client = GeminiApiClient(
            Settings(api_key="test-key", request_timeout_seconds=120)
        )

        with self.assertRaisesRegex(
            RuntimeError,
            "timed out after 120 seconds.*GEMINI_REQUEST_TIMEOUT_SECONDS",
        ):
            client.generate("review this", "reviewer")


if __name__ == "__main__":
    unittest.main()
