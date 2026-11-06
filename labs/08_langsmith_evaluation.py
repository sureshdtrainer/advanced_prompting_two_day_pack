"""Lab 08: Create/reuse a LangSmith dataset and evaluate a live prompt.

Run from the project root:
    python labs/08_langsmith_evaluation.py

Requires OPENAI_API_KEY and LANGSMITH_API_KEY in .env.
"""
import os
from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise SystemExit("Set OPENAI_API_KEY in .env before running Lab 08.")
if not os.getenv("LANGSMITH_API_KEY"):
    raise SystemExit("Set LANGSMITH_API_KEY in .env before running Lab 08.")

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATASET_NAME = "vehicle-defect-prompt-evaluation-v1"

examples = [
    {
        "inputs": {"inspection_text": "Fresh engine oil is visible beneath the front of the vehicle."},
        "outputs": {"category": "Fluid Leakage", "review_required": False},
    },
    {
        "inputs": {"inspection_text": "The brake pedal travels unusually far and feels soft."},
        "outputs": {"category": "Braking System", "review_required": False},
    },
    {
        "inputs": {"inspection_text": "The report says only: 'vehicle making a strange noise'."},
        "outputs": {"category": "Human Review", "review_required": True},
    },
    {
        "inputs": {"inspection_text": "Paint is peeling from the bonnet; no other issue is reported."},
        "outputs": {"category": "Paint Damage", "review_required": False},
    },
]

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You classify vehicle inspection observations. Choose exactly one category from: "
     "Paint Damage, Fluid Leakage, Braking System, Electrical System, Human Review. "
     "If evidence is vague or insufficient, choose Human Review and set review_required=true. "
     "Return only JSON with keys category and review_required."),
    ("human", "Inspection observation: {inspection_text}")
])

model = ChatOpenAI(model=MODEL_NAME, temperature=0)
chain = prompt | model

def target(inputs: dict) -> dict:
    """LangSmith target function: receives dataset inputs and returns predictions."""
    response = chain.invoke(inputs)
    # Parse a simple JSON response; fail visibly if the model returns invalid JSON.
    import json
    content = response.content
    if isinstance(content, list):
        content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
    text = str(content).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    prediction = json.loads(text)
    return {
        "category": prediction.get("category"),
        "review_required": prediction.get("review_required"),
    }

def category_match(run, example) -> dict:
    expected = example.outputs.get("category")
    actual = (run.outputs or {}).get("category")
    return {"key": "category_match", "score": float(actual == expected)}

def review_flag_match(run, example) -> dict:
    expected = example.outputs.get("review_required")
    actual = (run.outputs or {}).get("review_required")
    return {"key": "review_flag_match", "score": float(actual is expected)}

client = Client()
try:
    dataset = client.read_dataset(dataset_name=DATASET_NAME)
    print(f"Reusing existing LangSmith dataset: {DATASET_NAME}")
except Exception:
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Small classroom dataset for vehicle-defect prompt evaluation.",
    )
    client.create_examples(
        dataset_id=dataset.id,
        examples=examples,
    )
    print(f"Created LangSmith dataset: {DATASET_NAME}")

print("Starting LangSmith evaluation...")
results = evaluate(
    target,
    data=DATASET_NAME,
    evaluators=[category_match, review_flag_match],
    experiment_prefix="vehicle-defect-prompt",
    metadata={"prompt_version": "1.0.0", "model": MODEL_NAME},
)
print("Evaluation submitted. Open the LangSmith project/dataset to inspect examples, traces and scores.")
print(results)
