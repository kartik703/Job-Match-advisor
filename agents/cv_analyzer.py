# agents/cv_analyzer.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # <- UPDATED
from langchain.prompts import PromptTemplate
from tools.pdf_reader import extract_text_from_pdf

load_dotenv()  # Load .env file
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-4",
    openai_api_key=api_key  # <- PASSING THE API KEY
)

CV_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["resume_text"],
    template="""
You are a resume expert. Analyze this resume and extract:
1. Name
2. Education
3. Skills (keywords)
4. Experience (job titles + summary)

Resume:
{resume_text}

Respond in bullet points.
"""
)

def analyze_cv(cv_path: str):
    text = extract_text_from_pdf(cv_path)
    prompt = CV_ANALYSIS_PROMPT.format(resume_text=text[:4000])
    return llm.invoke(prompt)
