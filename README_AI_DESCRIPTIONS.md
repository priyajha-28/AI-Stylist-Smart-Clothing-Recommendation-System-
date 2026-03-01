
AI Descriptions Module
----------------------

This project includes `llm_descriptions.py`, which helps generate per-outfit
description JSON files following the exact AI-compatible prompt you supplied.

Files added:
- llm_descriptions.py : builds the prompt and includes a mock generator.
- descriptions/        : output folder where generated JSON files will be saved when run.

Usage:
1. Install dependencies (if calling a real LLM) and set OPENAI_API_KEY in environment.
2. From project root, run:
   python llm_descriptions.py
   This will create JSON description files for every PNG in uploads/.

Notes:
- The current version contains a local mock generator to produce valid JSON
  outputs immediately without requiring API keys. Replace the `mock_generate_for_filename`
  implementation with a real LLM call in `call_llm` if you want live AI outputs.
- Generated JSON follows the exact schema you requested and is safe to insert into templates.
