from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [
    {"report": "Oil is leaking under the engine.", "category": "Fluid Leakage"},
    {"report": "Paint is peeling from the bonnet.", "category": "Paint Damage"},
    {"report": "Brake pedal feels soft.", "category": "Braking System"},
]
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "Report: {report}"),
    ("ai", "Category: {category}")
])
few_shot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify only into the demonstrated categories. Do not invent root causes."),
    few_shot,
    ("human", "Report: {report}\nReturn category and evidence.")
])
print(final_prompt.format_messages(report="The bonnet paint is bubbling."))
