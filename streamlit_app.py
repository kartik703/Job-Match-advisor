import streamlit as st
import pandas as pd
import pdfplumber
from dotenv import load_dotenv
from agents.job_matcher import match_and_explain
from agents.live_cv_matcher import extract_text_from_pdf, calculate_similarity, explain_cv_match
from agents.career_mentor import get_career_mentorship
from agents.interview_coach import get_mock_interview_questions

load_dotenv()

st.set_page_config(page_title="Agentic Job Match Advisor", layout="wide")
st.title("🤖 Agentic Job Match Advisor")

# Four main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Match from DB",
    "🧾 Compare My CV",
    "🎓 Career Mentor",
    "🎤 Interview Coach"
])

# --- Tab 1: Match Job Description to Stored CVs ---
with tab1:
    st.subheader("📂 Match job description with stored CVs")

    job_description = ""
    upload = st.file_uploader("Upload job description (.txt or .pdf)", type=["txt", "pdf"], key="jd_upload1")
    if upload:
        if upload.type == "application/pdf":
            with pdfplumber.open(upload) as pdf:
                job_description = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        else:
            job_description = upload.read().decode("utf-8")
    else:
        job_description = st.text_area("Or paste job description here:", height=300, key="jd_textarea1")

    top_k = st.slider("Top CVs to return", 1, 10, 3)

    if st.button("🚀 Match from CV DB") and job_description:
        with st.spinner("Matching..."):
            matches = match_and_explain(job_description, top_k=top_k)

        results_df = []
        for i, match in enumerate(matches, 1):
            st.subheader(f"#{i}: {match['file_name']}")
            st.markdown(match["explanation"])
            results_df.append({"Rank": i, "File": match["file_name"], "Explanation": match["explanation"]})
            st.markdown("---")

        df = pd.DataFrame(results_df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Results as CSV", csv, "job_match_results.csv", "text/csv")

# --- Tab 2: Compare Live CV to Job Description ---
with tab2:
    st.subheader("🧾 Upload Your CV & Compare with Job")

    uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"], key="cv_upload")
    job_text = st.text_area("Paste the job description", height=300, key="jd_textarea2")

    if st.button("⚡ Compare CV to Job") and uploaded_cv and job_text:
        with st.spinner("Analyzing..."):
            cv_text = extract_text_from_pdf(uploaded_cv)
            score = calculate_similarity(cv_text, job_text)
            explanation = explain_cv_match(cv_text, job_text)

        st.success(f"Match Score: {score * 100:.1f}%")
        st.markdown("### 🤖 AI Match Evaluation")
        st.markdown(explanation)

# --- Tab 3: Career Mentor ---
with tab3:
    st.subheader("🎓 Career Mentor")
    uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"], key="mentor_cv")

    if st.button("🧠 Get Career Advice") and uploaded_cv:
        with st.spinner("Analyzing your CV..."):
            cv_text = extract_text_from_pdf(uploaded_cv)
            advice = get_career_mentorship(cv_text)

        st.success("✅ Advice generated!")
        st.markdown(advice)

# --- Tab 4: Interview Coach ---
with tab4:
    st.subheader("🎤 Interview Coach")
    uploaded_cv = st.file_uploader("Upload your CV (PDF)", type=["pdf"], key="interview_cv")
    job_desc = st.text_area("Paste job description", height=250, key="interview_job")

    if st.button("🎯 Generate Mock Interview") and uploaded_cv and job_desc:
        with st.spinner("Preparing questions..."):
            cv_text = extract_text_from_pdf(uploaded_cv)
            questions = get_mock_interview_questions(cv_text, job_desc)

        st.success("✅ Interview questions ready!")
        st.markdown(questions)
