import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Load .env file for OpenAI key
load_dotenv()

# Load FAISS index
faiss_index = FAISS.load_local(
    "cv_faiss_index", 
    OpenAIEmbeddings(), 
    allow_dangerous_deserialization=True
)

# Load LLM for explanations
llm = ChatOpenAI(temperature=0.3, model="gpt-4")

def find_top_matches(job_description, k=3):
    print(f"🔍 Matching job description against {k} CVs...")
    matches = faiss_index.similarity_search(job_description, k=k)
    return matches

def explain_match(cv_text, job_description):
    prompt = f"""
You are a helpful AI career advisor. Compare the following resume with the job description and explain in 5 bullet points why this candidate is a good or bad fit.

Resume:
{cv_text}

Job Description:
{job_description}
"""
    return llm.invoke(prompt)

def match_and_explain(job_description, top_k=3):
    top_matches = find_top_matches(job_description, k=top_k)
    results = []
    for match in top_matches:
        explanation = explain_match(match.page_content, job_description)
        results.append({
            "file_name": match.metadata.get("source", "Unknown"),
            "explanation": explanation.content if hasattr(explanation, 'content') else explanation
        })
    return results

if __name__ == "__main__":
    print("📄 Enter the job description below. Press Enter twice to submit.")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    job_desc = "\n".join(lines)

    output = match_and_explain(job_desc, top_k=3)
    
    print("\n🎯 Top Matching CVs:\n")
    for idx, res in enumerate(output, 1):
        print(f"#{idx}: {res['file_name']}")
        print(res["explanation"])
        print("-" * 60)
