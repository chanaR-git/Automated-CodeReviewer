import unittest

from pydantic import ValidationError

from src.agent.core import CodeReviewAgent
from src.agent.state import ReviewResult


class FakeContentGenerator:
    def __init__(self, response: str) -> None:
        self.response = response
        self.prompt: str | None = None
        self.system_instruction: str | None = None

    def generate(self, prompt: str, system_instruction: str) -> str:
        self.prompt = prompt
        self.system_instruction = system_instruction
        return self.response


class CodeReviewAgentTests(unittest.TestCase):
    def test_review_validates_and_returns_structured_findings(self) -> None:
        generator = FakeContentGenerator(
            '{"summary":"One issue found","findings":['
            '{"severity":"high","line":4,"issue":"Unsafe input",'
            '"recommendation":"Validate input"}]}'
        )

        result = CodeReviewAgent(generator).review("run(user_input)")

        self.assertIsInstance(result, ReviewResult)
        self.assertEqual(result.findings[0].severity, "high")
        self.assertIn("run(user_input)", generator.prompt or "")
        self.assertTrue(generator.system_instruction)

    def test_review_rejects_malformed_response(self) -> None:
        agent = CodeReviewAgent(FakeContentGenerator('{"summary": 4}'))

        with self.assertRaises(ValidationError):
            agent.review("pass")


if __name__ == "__main__":
    unittest.main()
