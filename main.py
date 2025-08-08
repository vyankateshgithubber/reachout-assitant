import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from docx import Document
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai
from uuid import uuid4
import asyncio

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

# Store resumes in-memory for demo (use a persistent store for production)
resume_store = {}

@app.get("/resume-ids")
async def get_resume_ids():
    # Return a list of resume IDs and a short preview of the resume text
    return [
        {"id": rid, "preview": resume_store[rid][:60].replace("\n", " ") + "..."}
        for rid in resume_store
    ]

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_stream = BytesIO(file_bytes)
    resume_text = ""

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

        # Generate a unique resume_id and store the text
        resume_id = str(uuid4())
        resume_store[resume_id] = resume_text

        return {"message": "Resume uploaded and parsed successfully.", "resume_id": resume_id}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/generate-message")
async def generate_message(
    message_type: str = Form(...),
    tone: str = Form(...),
    job_link: str = Form(""),
    target_profile: str = Form(""),
    resume_id: str = Form(...)
):
    resume_text = resume_store.get(resume_id)
    if not resume_text:
        return JSONResponse(content={"error": "Resume not found. Please upload again."}, status_code=400)

    prompt = f"""
You are an AI assistant creating personalized LinkedIn outreach messages.

Resume: 
{resume_text}

Message Type: {message_type}
Tone: {tone}
"""

    if target_profile:
        prompt += f"\nTarget Profile Info: {target_profile}"

    if job_link:
        prompt += f"\nJob Link : {job_link}"
    prompt += "\nGenerate the LinkedIn message accordingly."

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Use streaming
        def gen_chunks():
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text
        return StreamingResponse(gen_chunks(), media_type="text/plain")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def read_index():
    return FileResponse("templates/index.html")
