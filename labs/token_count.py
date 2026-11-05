import tiktoken
text = """You are a vehicle inspection assistant.Classify the defect using only the evidence provided."""
encoding = tiktoken.encoding_for_model("gpt-4o-mini")
tokens = encoding.encode(text)
print("Token count:", len(tokens))