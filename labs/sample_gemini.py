#import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

API_KEY = "GOOGLE_API_KEY"  # Replace with your actual Google API key

# Force REST transport at the Google SDK level
#genai.configure(api_key=API_KEY, transport="rest")

# Initialize LangChain model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=API_KEY
)

response = llm.invoke("Hello, are you working?")
print(response.content)
