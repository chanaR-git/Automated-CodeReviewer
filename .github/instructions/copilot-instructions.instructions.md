# Automated-CodeReviewer - Architecture & Development Guidelines

This document establishes the architecture standards, project structure, and coding conventions for **Automated-CodeReviewer**—an autonomous, agentic code-review and quality assurance platform built with LLMs and the Model Context Protocol (MCP).

All code generated or modified by AI assistants must strictly adhere to the guidelines set forth below.

---

## 1. System Architecture & Core Principles

Automated-CodeReviewer operates as a decoupled, event-driven agentic framework:

* **Agentic Loop (ReAct / Plan-and-Solve):** The core engine processes inputs, decides which tools to invoke via LLM Function Calling, evaluates tool execution results, and iterates until task completion.
* **Deterministic Execution:** LLM decisions guide flow, but all side effects (file reads, test runs, static analysis) are executed deterministically via isolated Python services or MCP tools.
* **Model Context Protocol (MCP):** Interaction with GitHub, local filesystems, and external tooling must be mediated through standard MCP server connections.
* **Model Agnosticism:** LLM integrations must rely on unified client abstractions (e.g., official `google-genai` SDK or unified interfaces like `LiteLLM`) to allow seamless switching between models.

---

## 2. Directory Structure

The repository maintains a strict modular layout. Do not place business logic inside entrypoints or script root directories.

```text
automated-code-reviewer/
├── .github/
│   ├── copilot-instructions.md
│   └── instructions/
│       ├── mcp-integration.md
│       └── testing-standards.md
├── src/
│   ├── agent/
│   │   ├── core.py           # Main Agentic Loop & Orchestration
│   │   ├── prompts.py        # System instructions & prompt templates
│   │   └── state.py          # State tracking & execution memory
│   ├── tools/
│   │   ├── base.py           # Base Tool interface/abstract class
│   │   ├── linter.py         # Static analysis tools (flake8/eslint)
│   │   ├── tester.py         # Test execution engines (pytest/jest)
│   │   └── github_mcp.py     # MCP client integrations for GitHub
│   ├── llm/
│   │   ├── client.py         # LLM SDK instantiation & wrapper
│   │   └── config.py         # Model parameters & safety settings
│   └── utils/
│       ├── logger.py         # Structured JSON logging
│       └── config.py         # Environment variables & runtime settings
├── tests/
│   ├── unit/                 # Unit tests for tools and utils
│   ├── integration/          # Integration tests for LLM flows & MCP
│   └── fixtures/             # Sample code repositories for testing
├── requirements.txt
└── README.md
```

---

## 3. Coding Conventions & Code Quality

1. **Language & Version:** Python 3.11+.
2. **Type Safety:** 100% type annotation coverage using standard `typing` modules or Python 3.9+ built-in generics. All public functions and methods must declare explicit parameter and return types.
3. **Structured Outputs:** All tool calls and final agent outputs must adhere to strictly validated schemas (using Pydantic `BaseModel`).
4. **Error Handling & Resilience:**
   * Never crash the Agentic Loop on tool failures. Wrap execution in structured error handlers and return the error trace back to the LLM for self-correction.
   * Enforce timeout limits on external process calls (e.g., subprocess linter runs).
5. **Configuration & Secrets:** Never hardcode API keys or system paths. Use environment variables (`GEMINI_API_KEY`, etc.) loaded via Pydantic `BaseSettings`.

---

## 4. Development Workflow Checklist

When adding a new feature or tool:
- [ ] Define the tool interface in `src/tools/` using strong type hints and docstrings.
- [ ] Register the tool cleanly with the LLM client configuration.
- [ ] Add corresponding unit tests under `tests/unit/`.
- [ ] Ensure the tool gracefully handles missing files, execution timeouts, and syntax errors.