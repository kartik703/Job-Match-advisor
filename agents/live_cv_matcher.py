import pdfplumber
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

embedding_model = OpenAIEmbeddings()
llm = ChatOpenAI(temperature=0.3, model="gpt-4")

def extract_text_from_pdf(uploaded_pdf):
    with pdfplumber.open(uploaded_pdf) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def calculate_similarity(text1, text2):
    vecs = embedding_model.embed_documents([text1, text2])
    sim_score = cosine_similarity([vecs[0]], [vecs[1]])[0][0]
    return round(sim_score, 3)

def explain_cv_match(cv_text, job_description):
    prompt = f"""
You're an AI recruiter. A candidate uploaded this resume:

{cv_text}

Compare it to this job description:

{job_description}

Evaluate the fit in 5 clear bullet points. Highlight technical skills, relevance, and missing gaps.
"""
    return llm.invoke(prompt).content
