# Automated Code Reviewer

Two small command-line code-review agents use the same validated review workflow
with different Gemini integrations: the Gemini REST API (Python standard library) and Google's official `google-genai` SDK.

## Setup

Use Python 3.11 or later and install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Add your Gemini API key to the root `.env` file. `GEMINI_MODEL` and
`GEMINI_REQUEST_TIMEOUT_SECONDS` are also configured there and default to
`gemini-3.8-flash` and `120`, respectively. If a request times out, check your
network connection and increase `GEMINI_REQUEST_TIMEOUT_SECONDS` if needed.
Keep the `.env` file local; it is
excluded from Git.

## Run

Pass the path to the source file you want reviewed:

```powershell
python -m src.agent.gemini_api path\to\file.py
python -m src.agent.google_genai path\to\file.py
```

Both entry points print a JSON review with a summary and validated findings.
The first calls Gemini's `generateContent` REST endpoint directly; the second
uses the `google-genai` SDK.

## Test

```powershell
python -m unittest discover -s tests
```
