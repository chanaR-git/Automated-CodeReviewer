import io
import unittest
from contextlib import redirect_stderr
from unittest.mock import MagicMock, patch

from src.agent.cli import run_cli


class CliTests(unittest.TestCase):
    @patch("src.agent.cli.Path.read_text", return_value="source")
    @patch("src.agent.cli.get_settings")
    @patch("src.agent.cli.GeminiApiClient")
    @patch("src.agent.cli.CodeReviewAgent")
    def test_api_error_is_reported_without_traceback(
        self,
        mock_agent: MagicMock,
        _mock_client: MagicMock,
        _mock_settings: MagicMock,
        _mock_read_text: MagicMock,
    ) -> None:
        mock_agent.return_value.review.side_effect = RuntimeError(
            "Gemini API request timed out after 120 seconds."
        )
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as error:
                run_cli("api", ["source.py"])

        self.assertEqual(error.exception.code, 1)
        self.assertIn(
            "Error: Gemini API request timed out after 120 seconds.", stderr.getvalue()
        )
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
