import streamlit as st
import os
from utils.gemini import ask_gemini
from utils.pdf_parser import extract_text_from_pdf
from utils.embeddings import embed_chunks
from utils.vector_store import save_vectorstore, search_similar_chunks


st.markdown("""
<style>
/* Hide Streamlit footer */
footer {visibility: hidden;}

/* Make input fields look better */
.stTextArea textarea, .stTextInput input {
    border-radius: 10px;
    padding: 0.5rem;
}

/* Buttons */
.stButton>button {
    border-radius: 8px;
    background-color: #1e88e5;
    color: white;
    font-weight: bold;
    transition: 0.2s ease-in-out;
}
.stButton>button:hover {
    background-color: #1565c0;
}

/* Center the header */
h1 {
    text-align: center;
    font-size: 2.5rem;
}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────── Config ──────────────────────────────
st.set_page_config(page_title="AI Career Tutor", layout="wide")
st.title(" AI Career Tutor")

# ────────────────────────────── Ensure upload directory exists ──────────────────────────────
UPLOAD_DIR = os.path.join("data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ────────────────────────────── Session State ──────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

# ────────────────────────────── Sidebar Tools ──────────────────────────────
with st.sidebar:
    st.header("📂 Career Tools")
    selected_tool = st.radio("Select a tool to use:", [
        "💬 General Chat",
        "📄 Cover Letter Generator",
        "📋 Resume Analyzer",
        "📌 JD Analyzer",
        "🎤 Mock Interview"
    ])
    st.markdown("---")
    if st.button("🆕 New Chat"):
        st.session_state.history = []
        st.rerun()
    
    st.markdown("<div style='height:220px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <hr style="margin: 0.5rem 0;">
    <div style="text-align: center; font-size: 11px; color: gray;">
        Built by <strong>Jaiganesh V</strong><br>
        <a href="mailto:jaiganesh362@gmail.com" target="_blank">Gmail</a> &nbsp; | &nbsp;
        <a href="https://www.linkedin.com/in/jai-ganesh-1v" target="_blank">LinkedIn</a> &nbsp; | &nbsp;
        <a href="https://github.com/jaiganesh362" target="_blank">GitHub</a>
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────────── PDF Upload Handler ──────────────────────────────
with st.expander("📎 Upload PDF (Resume / Notes / JD)", expanded=False):
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file:
        save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("Processing PDF..."):
            text = extract_text_from_pdf(save_path)
            chunks = text.split("\n\n")
            vectors = embed_chunks(chunks)
            save_vectorstore(vectors, chunks)
            st.session_state.pdf_uploaded = True

        st.success("✅ PDF uploaded and indexed!")


# ────────────────────────────── General Chat ──────────────────────────────
if selected_tool == "💬 General Chat":
    st.subheader("💬 Start chatting with your Career Coach")

    user_input = st.chat_input("Ask anything... (e.g., 'Tips for my resume')")
    if user_input:
        with st.spinner("Thinking..."):
            if st.session_state.pdf_uploaded:
                similar_chunks = search_similar_chunks(user_input)
                context = "\n\n".join(similar_chunks)
                prompt = f"""Use the context below to answer the question:

Context:
{context}

Question: {user_input}
"""
            else:
                prompt = user_input

            reply = ask_gemini(prompt)

        st.session_state.history.append(("🧑‍💼 You", user_input))
        st.session_state.history.append(("🤖 Coach", reply))

    for speaker, msg in st.session_state.history[::-1]:
        st.markdown(f"**{speaker}:** {msg}")


# ────────────────────────────── Cover Letter Generator ──────────────────────────────
elif selected_tool == "📄 Cover Letter Generator":
    st.subheader("📄 Generate a Cover Letter")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="cover_resume")
    jd = st.text_area("Paste Job Description", height=250)

    if st.button("▶️ Generate Cover Letter"):
        if not resume_file or not jd.strip():
            st.warning("Please upload resume and paste job description.")
        else:
            with st.spinner("Generating cover letter..."):
                path = os.path.join(UPLOAD_DIR, resume_file.name)
                with open(path, "wb") as f:
                    f.write(resume_file.read())
                resume_text = extract_text_from_pdf(path)

                prompt = f"""You're a professional career coach. Based on the resume and job description below, write a personalized, ATS-friendly cover letter.

Resume:
{resume_text}

Job Description:
{jd}
"""
                letter = ask_gemini(prompt)

            st.success("✅ Cover Letter Ready!")
            st.text_area("📄 Cover Letter", value=letter, height=350)
            st.download_button("📥 Download", data=letter, file_name="cover_letter.txt")


# ────────────────────────────── Resume Analyzer ──────────────────────────────
elif selected_tool == "📋 Resume Analyzer":
    st.subheader("📋 Resume Analyzer")

    resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"], key="analyze_resume")

    if st.button("🔍 Analyze Resume"):
        if not resume_file:
            st.warning("Please upload your resume first.")
        else:
            with st.spinner("Analyzing resume..."):
                path = os.path.join(UPLOAD_DIR, resume_file.name)
                with open(path, "wb") as f:
                    f.write(resume_file.read())

                resume_text = extract_text_from_pdf(path)

                prompt = f"""
You are an ATS and career coach. Carefully analyze this resume and give:

- ✅ Key strengths
- ⚠️ Weaknesses or areas to improve
- 📌 Suggestions to improve format, keywords, layout

Resume:
{resume_text}
"""

                feedback = ask_gemini(prompt)

            st.success("✅ Analysis Complete!")
            st.text_area("📋 Gemini Feedback", value=feedback, height=350)


# ────────────────────────────── JD Analyzer ──────────────────────────────
elif selected_tool == "📌 JD Analyzer":
    st.subheader("📌 Job Description Analyzer")

    job_desc = st.text_area("Paste Job Description", height=300)

    if st.button("🔍 Analyze JD"):
        if not job_desc.strip():
            st.warning("Please paste a job description.")
        else:
            with st.spinner("Analyzing JD..."):
                prompt = f"""
You are a career expert. Analyze the following job description and list:

- ✅ Key skills and technologies required
- 📌 Keywords candidates should include in resume
- 💡 Tips to tailor a resume for this JD

Job Description:
{job_desc}
"""
                jd_analysis = ask_gemini(prompt)

            st.success("✅ JD Analysis Complete!")
            st.text_area("📌 Gemini's Analysis", value=jd_analysis, height=350)


# ────────────────────────────── Mock Interview ──────────────────────────────
elif selected_tool == "🎤 Mock Interview":
    st.subheader("🎤 Mock Interview Practice")

    role = st.text_input("Enter the role you're preparing for (e.g., Data Analyst, SDE)")

    if "mock_chat" not in st.session_state:
        st.session_state.mock_chat = []
        st.session_state.next_question = ""

    if st.button("🎙️ Start Interview") and role:
        with st.spinner("Generating first question..."):
            prompt = f"You are an interviewer. Ask the first interview question for a {role} candidate."
            st.session_state.next_question = ask_gemini(prompt)
            st.session_state.mock_chat.append(("🧑 Interviewer", st.session_state.next_question))

    if st.session_state.next_question:
        st.markdown(f"**🧑 Interviewer:** {st.session_state.next_question}")
        user_answer = st.text_area("Your Answer", key="answer_area")

        if st.button("📩 Submit Answer"):
            with st.spinner("Evaluating..."):
                feedback_prompt = f"""You are the interviewer. Here is the candidate's answer to your question.

Question: {st.session_state.next_question}
Answer: {user_answer}

Give:
- ✅ Strengths
- ⚠️ Weaknesses
- 📌 How they can improve
Then ask the next interview question."""
                response = ask_gemini(feedback_prompt)

                # Split response into feedback + next question
                parts = response.split("Next Question:", 1)
                feedback = parts[0].strip()
                next_q = parts[1].strip() if len(parts) > 1 else ""

                st.session_state.mock_chat.append(("🧑 You", user_answer))
                st.session_state.mock_chat.append(("🤖 Feedback", feedback))

                if next_q:
                    st.session_state.next_question = next_q
                    st.session_state.mock_chat.append(("🧑 Interviewer", next_q))
                else:
                    st.session_state.next_question = ""

    for speaker, msg in st.session_state.mock_chat[::-1]:
        st.markdown(f"**{speaker}:** {msg}")
