"""Lab 09: LLM-as-a-Judge using an explicit evaluation rubric.

Run from the project root:
    python labs/09_llm_as_judge.py

Requires OPENAI_API_KEY in .env.
"""
import json
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("Set OPENAI_API_KEY in .env before running Lab 09.")

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
judge = ChatOpenAI(model=MODEL_NAME, temperature=0)

rubric = """
Score the answer against the reference answer and the user's request.
Use integer scores from 1 to 5:
- factual_alignment: Does the answer agree with the reference and avoid unsupported claims?
- completeness: Does it address the important parts of the request?
- instruction_following: Does it follow the requested format and constraints?
- evidence_handling: Does it distinguish known evidence from uncertainty?

A score of 1 is poor, 3 is mixed/partially acceptable, and 5 is strong.
Do not reward confident wording by itself. If the answer invents a fact that conflicts
with the reference, reduce factual_alignment. If the reference is insufficient to decide,
say so in the rationale rather than guessing.

Return only valid JSON with this schema:
{
  "factual_alignment": 1,
  "completeness": 1,
  "instruction_following": 1,
  "evidence_handling": 1,
  "overall": 1,
  "rationale": "brief explanation",
  "needs_human_review": true
}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a careful evaluator. Apply the rubric consistently.\n{rubric}"),
    ("human",
     "USER REQUEST:\n{question}\n\nREFERENCE:\n{reference}\n\nCANDIDATE ANSWER:\n{answer}")
])
chain = prompt | judge

samples = [
    {
        "question": "What category should be assigned to the observation?",
        "reference": "The observation reports fresh oil beneath the engine. Category: Fluid Leakage.",
        "answer": "Category: Fluid Leakage. Evidence: fresh oil beneath the engine.",
    },
    {
        "question": "What category should be assigned to the observation?",
        "reference": "The report only says 'strange noise'. The evidence is insufficient; route to Human Review.",
        "answer": "This is definitely a transmission failure and the vehicle is unsafe to drive.",
    },
]

def parse_json(content):
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    text = str(content).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    return json.loads(text)

for index, sample in enumerate(samples, start=1):
    response = chain.invoke({"rubric": rubric, **sample})
    scores = parse_json(response.content)
    print(f"\n--- Sample {index} ---")
    print(json.dumps(scores, indent=2))
    print("\nInterpretation:")
    print("- Treat the scores as a review aid, not an objective truth.")
    print("- Compare judge results with a human-reviewed gold set.")
    print("- Investigate large disagreement between human and judge ratings.")

print("\nCalibration exercise: independently score both samples, then compare your scores with the judge.")
