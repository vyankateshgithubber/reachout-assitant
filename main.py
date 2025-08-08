import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/app", StaticFiles(directory="templates", html=True), name="frontend")

resume_text = ""


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    global resume_text
    resume_text = ""

    file_bytes = await file.read()
    file_stream = BytesIO(file_bytes)

    try:
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file_stream)
            resume_text = "\n".join(page.extract_text() or "" for page in reader.pages)

        elif file.filename.endswith(".docx"):
            document = Document(file_stream)
            resume_text = "\n".join(para.text for para in document.paragraphs)

        else:
            return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

        if not resume_text.strip():
            return JSONResponse(content={"error": "Could not extract any text from the file."}, status_code=400)

        return {"message": "Resume uploaded and parsed successfully."}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/generate-message")
async def generate_message(
    message_type: str = Form(...),
    tone: str = Form(...),
    target_profile: str = Form("")
):
    global resume_text

    if not resume_text:
        return JSONResponse(content={"error": "Resume not uploaded yet."}, status_code=400)

    prompt = f"""
You are an AI assistant creating personalized LinkedIn outreach messages.

Resume: 
{resume_text}

Message Type: {message_type}
Tone: {tone}
"""

    if target_profile:
        prompt += f"\nTarget Profile Info: {target_profile}"

    prompt += "\nGenerate the LinkedIn message accordingly."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        message = response.text.strip()
        return {"message": message}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
def read_index():
    return FileResponse("templates/index.html")
