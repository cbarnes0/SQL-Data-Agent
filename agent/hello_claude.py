"""Phase 0 checkpoint: confirm a hello-world Anthropic API call works.

Usage (from repo root):
    uv run --project agent python agent/hello_claude.py
"""

from pathlib import Path

import anthropic
from dotenv import load_dotenv

# .env lives at the repo root
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=256,
    messages=[
        {
            "role": "user",
            "content": "Reply with one sentence confirming the SQL Data Agent project's API access works.",
        }
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)

print(
    f"\n[usage] input={response.usage.input_tokens} tokens, "
    f"output={response.usage.output_tokens} tokens, model={response.model}"
)
