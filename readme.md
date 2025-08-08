# 🤖 LinkedIn Outreach Assistant (AI-Powered)

This project is an intelligent web assistant that helps you generate **personalized LinkedIn messages** such as:

- Referral requests
- Recruiter introductions
- Networking messages

All generated using **Google Gemini (`gemini-1.5-flash`)** based on your uploaded **resume** and optional **target LinkedIn profile** or **job link**.

---

## 🌟 Features

- ✅ Upload your resume (PDF or DOCX)
- ✅ Select message type
- ✅ Optional: Provide a target LinkedIn profile URL
- ✅ Optional: Provide a job link for referral requests
- ✅ Automatically crafts a clean, human-like message using Gemini
- ✅ Clean & elegant UI
- ✅ Built with FastAPI + HTML/CSS/JS

---

## 🚀 Demo

https://localhost:8000 (when running locally)

---

## 🧠 Powered By

- [Google Gemini 1.5 Flash](https://ai.google.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [python-docx](https://pypi.org/project/python-docx/)

---

## 🛠️ How It Works

1. Upload your resume file (PDF/DOCX)
2. Select message type (Referral, Recruiter, Networking)
3. (Optional) Enter job link or target profile
4. App sends everything to Gemini API
5. Gemini generates a personalized, polished LinkedIn message
6. You review and copy the result

---

## 📁 Project Structure

```
project-root/
│
├── main.py                 # FastAPI backend
├── .env                    # Gemini API key
├── templates/
│   └── index.html          # Frontend UI
│
├── static/
│   └── styles.css          # Elegant CSS styling
│
└── README.md               # This file
```

---

## 🔐 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/linkedin-outreach-assistant.git
cd linkedin-outreach-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn python-docx PyPDF2 python-multipart google-generativeai python-dotenv
```

### 3. Set your Gemini API key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

Get your API key from:  
👉 https://makersuite.google.com/app/apikey

---

## ▶️ Run the App

```bash
uvicorn main:app --reload
```

Open in your browser:  
👉 http://localhost:8000

---

## 📷 Screenshots

| Upload Resume | Generated Message |
|---------------|-------------------|
| ![upload](docs/upload.png) | ![output](docs/output.png) |

---

## ✨ Example Output

**Referral Request:**

> Hi [Name], I came across the [Job Link] and was very interested in the opportunity at [Company]. Based on my experience in [domain], I believe I could be a great fit. I'd be grateful if you could consider referring me. Happy to provide more info. Thanks in advance!

---

## 💡 Future Improvements

- Save message history
- Direct LinkedIn integration
- Add tone options (formal, casual)
- Add resume parsing with LangChain

---

## 👨‍💻 Author

Made with 💙 by Vyankatesh

