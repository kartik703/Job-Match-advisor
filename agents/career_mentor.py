from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-4", temperature=0.4)

def get_career_mentorship(cv_text):
    prompt = f"""
You are a seasoned career mentor helping professionals improve their career prospects.

Here is a resume:
{cv_text}

Give personalized career advice in bullet points. Focus on:
- Skill gaps and what to learn next
- Career paths that align with experience
- Certifications or tools to pick up
- Suggestions for portfolio or personal projects
"""
    return llm.invoke(prompt).content

# Example (for CLI testing)
if __name__ == "__main__":
    with open("data/resume_samples/Kartik_Goswami_AfternoonFinance_AIEngineer_CV.pdf", "r") as f:
        text = f.read()
    print(get_career_mentorship(text))
