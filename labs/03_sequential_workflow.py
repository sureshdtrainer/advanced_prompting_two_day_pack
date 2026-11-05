import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

load_dotenv(override=True)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "Missing OPENAI_API_KEY. Copy .env.example to .env and set OPENAI_API_KEY=... "
        "(or set OPENAI_API_KEY in your environment) before running this lab."
    )

model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
extract = ChatPromptTemplate.from_template(
    "Extract only stated symptoms from this report. Do not infer causes. Report: {report}"
) | model | StrOutputParser()
classify = ChatPromptTemplate.from_template(
    "Choose one category: Paint Damage, Fluid Leakage, Braking System, "
    "Electrical System, Human Review. If evidence is insufficient, choose Human Review. "
    "Symptoms: {symptoms}. Return category and supporting evidence."
) | model | StrOutputParser()

report = "Oil is leaking beneath the engine."
symptoms = extract.invoke({"report": report})
result = classify.invoke({"symptoms": symptoms})
print("Extracted symptoms:", symptoms)
print("Classification:", result)
