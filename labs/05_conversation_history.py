from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a careful vehicle inspection assistant. Do not invent facts."),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])
history = [
    HumanMessage(content="Oil is leaking beneath the engine."),
    AIMessage(content="The reported symptom is oil leakage; its source is unknown.")
]
messages = prompt.format_messages(
    history=history,
    question="What evidence do we have?"
)
for message in messages:
    print(message.type, ":", message.content)

# This demonstrates explicit history insertion. Add a model call only when API access is configured.
