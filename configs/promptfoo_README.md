# Promptfoo optional evaluation

This configuration compares two dedicated prompt templates:
- `prompts/promptfoo_baseline.txt`
- `prompts/promptfoo_improved.txt`

They use the `{{inspection_text}}` variable expected by Promptfoo and do not modify the original Labs 01–07 prompt files.

Install Node.js, then run from the project root:

```powershell
npm install -g promptfoo
$env:OPENAI_API_KEY = "your-key"
promptfoo eval -c configs/promptfooconfig.yaml
promptfoo view
```

The simple `contains` checks demonstrate regression testing only. Improve the test suite with structured JSON assertions, expected output checks and human-reviewed cases before using it for consequential decisions.
