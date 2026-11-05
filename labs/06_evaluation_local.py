import json
from pathlib import Path

CASES = json.loads(Path("data/vehicle_defects.json").read_text(encoding="utf-8"))
ALLOWED = {"Paint Damage", "Fluid Leakage", "Braking System",
           "Electrical System", "Human Review"}

# Demonstration with illustrative predictions; replace with actual model outputs.
predictions = [
    {"category":"Fluid Leakage","evidence":"Oil observed beneath engine","review_required":False},
    {"category":"Paint Damage","evidence":"Paint peeling from bonnet","review_required":False},
    {"category":"Braking System","evidence":"Brake pedal feels soft","review_required":False},
    {"category":"Electrical System","evidence":"Warning light reported","review_required":False},
    {"category":"Human Review","evidence":"Report is vague","review_required":True},
]

correct = format_ok = alignment_ok = 0
for case, pred in zip(CASES, predictions):
    correct += int(pred["category"] == case["category"])
    format_ok += int(set(pred) == {"category","evidence","review_required"}
                     and isinstance(pred["review_required"], bool))
    alignment_ok += int(pred["category"] in ALLOWED)
print(f"Category accuracy: {correct}/{len(CASES)} = {correct/len(CASES):.0%}")
print(f"Format compliance: {format_ok}/{len(CASES)} = {format_ok/len(CASES):.0%}")
print(f"Allowed-category compliance: {alignment_ok}/{len(CASES)} = {alignment_ok/len(CASES):.0%}")
print("These are demonstration predictions, not a live LLM evaluation.")
