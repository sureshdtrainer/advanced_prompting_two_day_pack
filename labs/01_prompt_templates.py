from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

report = "Oil is leaking beneath the engine."

string_prompt = PromptTemplate.from_template(
    "Classify the vehicle defect. Report: {report}"
)
print("String prompt:")
print(string_prompt.format(report=report))

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a careful vehicle inspection assistant."),
    ("human", "Classify this report without inventing evidence: {report}")
])
print("\nChat messages:")
for message in chat_prompt.format_messages(report=report):
    print(message.type, ":", message.content)
