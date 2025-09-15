 
# 🧠 Ai-career-tutor — GenAI Career Assistant

An advanced career assistant powered by **Google Gemini 1.5 Flash**, **FAISS**, and **RAG (Retrieval-Augmented Generation)**. This ChatGPT-style web app helps job seekers generate cover letters, analyze resumes, extract insights from job descriptions, and even answer questions from uploaded PDFs.


<img width="1919" height="950" alt="demo" src="https://github.com/user-attachments/assets/062ba2ec-470a-4305-8aa3-3015b48499d4" />

---

## 🚀 Features

### 🧑‍💼 Career Tools
- **Cover Letter Generator** – Upload your resume and get a tailored letter  
- **Resume ATS Analyzer** – Upload and receive score + optimization tips  
- **Job Description Analyzer** – Paste JD and get keywords to add to your resume  
- **Mock Interview Chat** – Practice interview questions with AI feedback  

### 📄 PDF Upload & Q&A (RAG)
- Upload PDFs (e.g., ML notes, interview prep)  
- Ask questions from the file like:  
  > “Explain precision vs recall from the PDF”  
- Text is embedded using `sentence-transformers`  
- Stored in **FAISS**, retrieved based on similarity  
- Answer generated using **Gemini 1.5 Flash**

### 💬 Chat Interface (ChatGPT-style)
- Continuous conversation history  
- General AI Q&A enabled  
- Optional left sidebar to pick specific tools  
- `➕` icon to upload PDF — just like ChatGPT’s document upload

---

## 🧠 Tech Stack

| Tool                     | Usage                              |
|--------------------------|-------------------------------------|
| **Streamlit**            | Frontend Web UI                     |
| **Gemini 1.5 Flash**     | Generative responses (free API)     |
| **FAISS**                | Fast vector search (for RAG)        |
| **sentence-transformers**| Embedding PDF chunks                |
| **pdfplumber**           | PDF text extraction                 |
| **dotenv**               | Secure API key handling             |

---

## 📁 Project Structure

```
ai-career-coach/
├── app/
│   ├── main.py
│   ├── utils/
│   │   ├── gemini.py
│   │   ├── pdf_utils.py
│   │   ├── vector_store.py
├── data/
│   ├── uploads/           # PDF uploads (ignored in .gitignore)
│   └── faiss_index/       # FAISS data (ignored)
├── .env
├── .gitignore
├── requirements.txt
├── test_gemini.py
├── demo.png               # App screenshot
└── README.md
```

---

## 🔧 Setup & Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/jaiganesh362/AI-career-tutor.git
cd ai-career-coach
```

### 2️⃣ Create `.env` file

Create a `.env` file in the root folder:

```ini
GOOGLE_API_KEY=your_gemini_api_key_here
```

> ✅ You can get your free key from [Google AI Studio](https://makersuite.google.com/)

### 3️⃣ Create a virtual environment & install packages

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
python -m streamlit run app/main.py
```

---

## 🛡️ Safe & Clean Code

- `.env` and `data/` folders are excluded from Git using `.gitignore`  
- No sensitive info is committed  
- Code is modular and production-ready  

---

## 👤 About the Author

**Jaiganesh V**  
📧 [jaiganesh362@gmail.com](mailto:jaiganesh362@gmail.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/jai-ganesh-1v) | [GitHub](https://github.com/jaiganesh362)

---

## ⭐ Why This Project?

This project showcases:

- Real-world GenAI + RAG integration  
- Resume-enhancing use case for career platforms  
- Free-tier Gemini API with embeddings and FAISS  
- ChatGPT-style interface using Streamlit  
- Clean folder structure and scalable architecture  


