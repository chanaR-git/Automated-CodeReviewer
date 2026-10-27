import unittest
from unittest.mock import MagicMock, patch

from src.llm.config import Settings
from src.llm.google_genai import GoogleGenAIClient


class GoogleGenAIClientTests(unittest.TestCase):
    @patch("src.llm.google_genai.genai.Client")
    def test_generate_uses_sdk_and_returns_text(
        self,
        mock_client_factory: MagicMock,
    ) -> None:
        mock_client = mock_client_factory.return_value
        mock_client.models.generate_content.return_value.text = '{"summary":"Clean"}'
        client = GoogleGenAIClient(Settings(api_key="test-key"))

        result = client.generate("review this", "reviewer")

        self.assertEqual(result, '{"summary":"Clean"}')
        mock_client_factory.assert_called_once_with(api_key="test-key")
        call = mock_client.models.generate_content.call_args.kwargs
        self.assertEqual(call["model"], "gemini-3.8-flash")
        self.assertEqual(call["contents"], "review this")
        self.assertEqual(call["config"].system_instruction, "reviewer")
        self.assertEqual(call["config"].response_mime_type, "application/json")


if __name__ == "__main__":
    unittest.main()
