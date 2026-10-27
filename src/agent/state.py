from typing import Literal

from pydantic import BaseModel, ConfigDict


class ReviewFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    severity: Literal["critical", "high", "medium", "low", "info"]
    line: int | None
    issue: str
    recommendation: str


class ReviewResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    findings: list[ReviewFinding]
