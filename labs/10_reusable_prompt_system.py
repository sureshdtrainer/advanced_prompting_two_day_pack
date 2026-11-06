"""Lab 10: Reusable prompt components, YAML loading and prompt version metadata.

Run from the project root:
    python labs/10_reusable_prompt_system.py

No API key is required. This lab builds and prints a LangChain chat prompt.
"""
from pathlib import Path
import yaml
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
PROMPT_FILE = ROOT / "prompts" / "vehicle_classifier_v1.yaml"

def load_prompt_definition(path: Path) -> dict:
    """Load and validate the minimum metadata needed by this exercise."""
    definition = yaml.safe_load(path.read_text(encoding="utf-8"))
    required = {"name", "version", "description", "system", "human"}
    missing = required - set(definition or {})
    if missing:
        raise ValueError(f"Prompt definition is missing fields: {sorted(missing)}")
    return definition

def build_chat_prompt(definition: dict) -> ChatPromptTemplate:
    """Create a reusable chat prompt from an external definition."""
    return ChatPromptTemplate.from_messages([
        ("system", definition["system"]),
        ("human", definition["human"]),
    ])

def render_prompt(prompt: ChatPromptTemplate, inspection_text: str) -> str:
    """Render a prompt for inspection; this function does not call a model."""
    messages = prompt.format_messages(inspection_text=inspection_text)
    return "\n\n".join(f"{message.type.upper()}:\n{message.content}" for message in messages)

def validate_semver(version: str) -> bool:
    """Small classroom check for MAJOR.MINOR.PATCH version strings."""
    parts = version.split(".")
    return len(parts) == 3 and all(part.isdigit() for part in parts)

definition = load_prompt_definition(PROMPT_FILE)
prompt = build_chat_prompt(definition)

print(f"Prompt: {definition['name']}")
print(f"Version: {definition['version']}")
print(f"SemVer format valid: {validate_semver(definition['version'])}")
print(f"Description: {definition['description']}")
print("\n--- Rendered prompt ---")
print(render_prompt(
    prompt,
    "The brake pedal feels soft and travels farther than usual."
))

print("\nVersioning practice:")
print("PATCH: wording/typo change without intended behavior change.")
print("MINOR: backward-compatible capability or instruction addition.")
print("MAJOR: incompatible change to the prompt's expected behavior or output contract.")
print("Commit each meaningful change and record evaluation results alongside the version.")
