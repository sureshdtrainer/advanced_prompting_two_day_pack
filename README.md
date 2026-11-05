# Advanced Prompting Techniques — lab starter pack

## Before you start
- Python programming basics, basic LLM concepts and prompt-engineering terminology.
- VS Code and Python installed.
- Authorized model-provider API key, if running live model calls.
- LangSmith access only if the class will use tracing/datasets.
- Node.js and promptfoo only if the promptfoo module is in scope.

### Python version
This pack is tested with Python 3.12/3.13 on Windows. Some dependencies may not publish wheels immediately for very new Python versions; if you use a bleeding-edge Python, `pip install -r requirements.txt` may attempt to compile native extensions (requiring Microsoft C++ Build Tools).

## Windows PowerShell setup
```powershell
python --version
python -m venv .venv
# If activation fails with "running scripts is disabled", run ONE of:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
\.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` locally to add your authorized API key and model. Never commit `.env`.

If you prefer not to change execution policy, you can skip activation and run commands with the venv interpreter explicitly:
```powershell
\.\.venv\Scripts\python.exe -m pip install --upgrade pip
\.\.venv\Scripts\python.exe -m pip install -r requirements.txt
\.\.venv\Scripts\python.exe labs/01_prompt_templates.py
```

## Run the labs
Run commands from the project root, for example:
```powershell
python labs/01_prompt_templates.py
python labs/02_few_shot_patterns.py
python labs/04_self_consistency.py
python labs/05_conversation_history.py
python labs/06_evaluation_local.py
```
The sequential workflow lab calls a live model:
```powershell
python labs/03_sequential_workflow.py
```

Optional: If you want to use Google's Gemini instead of OpenAI, install the provider package and set these in `.env`:
- `LLM_PROVIDER=google`
- `GOOGLE_API_KEY=...`
- `GOOGLE_MODEL=gemini-3.8-flash`
```powershell
pip install langchain-google-genai
```

## API and version note
LangChain APIs evolve. This starter pack uses modern `langchain-core` runnable composition for sequential workflows and explicit message history. The course outline mentions legacy classes such as `SequentialChain` and `ConversationChain`; teach their concepts, and demonstrate legacy APIs only in a separately pinned environment if the client specifically requires those exact classes.

## Labs in this pack
1. String prompt vs chat prompt
2. Few-shot examples in chat prompts
3. Sequential extraction/classification workflow
4. Self-Consistency vote aggregation (mock outputs first)
5. Explicit conversation-history insertion
6. Deterministic evaluation metrics
7. Optional promptfoo readiness notes

## Safety and cost
- Never put keys in source code, notebooks, screenshots, or shared chat.
- Use small test cases and low-cost approved models.
- Do not treat model-generated explanations as verified facts.
- Evaluation data must include ambiguous cases and expected human-review behavior.
