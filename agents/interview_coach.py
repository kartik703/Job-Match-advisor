from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

def get_mock_interview_questions(cv_text, job_description):
    prompt = f"""
You're an AI mock interview coach. Based on the following resume and job description, generate 5 tailored interview questions and provide tips on how to answer them well.

Resume:
{cv_text}

Job Description:
{job_description}

Make the questions technical, behavioral, and strategic where relevant.
"""
    return llm.invoke(prompt).content

# CLI Example
if __name__ == "__main__":
    print(get_mock_interview_questions("My resume...", "Job at AI startup..."))
