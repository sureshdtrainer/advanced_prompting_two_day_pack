from collections import Counter

# First run with these mock outputs to learn the aggregation logic.
# Replace this list with validated model responses in the extension exercise.
candidates = [
    "Fluid Leakage", "Fluid Leakage", "Human Review",
    "Fluid Leakage", "Fluid Leakage"
]
allowed = {"Paint Damage", "Fluid Leakage", "Braking System",
           "Electrical System", "Human Review"}
valid = [c for c in candidates if c in allowed]
if not valid:
    raise ValueError("No valid candidate outputs.")

counts = Counter(valid)
winner, votes = counts.most_common(1)[0]
agreement = votes / len(valid)
print("Votes:", counts)
print("Selected:", winner, "agreement:", f"{agreement:.0%}")
if agreement < 0.8:
    print("Flag for human review: low agreement")

# Teaching note: agreement is not proof of correctness. Models may share errors.
