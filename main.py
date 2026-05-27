from fastapi import FastAPI, HTTPException, UploadFile, File
from schemas import TextRequest, AIResponse
from ai_service import summarize, extract_tasks, generate_reply
from dotenv import load_dotenv
load_dotenv()

import os
from typing import Optional
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
try:
    import docx
except ImportError:
    docx = None

app = FastAPI(
    def read_file_content(file: UploadFile) -> Optional[str]:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext == ".txt":
            return file.file.read().decode("utf-8", errors="ignore")
        elif ext == ".pdf" and PdfReader:
            reader = PdfReader(file.file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        elif ext in [".doc", ".docx"] and docx:
            doc = docx.Document(file.file)
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            return None

    @app.post("/upload_file", response_model=AIResponse)
    async def upload_file(file: UploadFile = File(...), action: str = "summarize"):
        """
        Upload a file (txt, pdf, docx) and process it (summarize, extract tasks, or search).
        action: summarize | tasks | reply
        """
        content = read_file_content(file)
        if not content:
            raise HTTPException(status_code=400, detail="Unsupported file type or failed to read file.")
        if action == "summarize":
            result = summarize(content)
            return {"result": result, "type": "summary"}
        elif action == "tasks":
            result = extract_tasks(content)
            return {"result": result, "type": "tasks"}
        elif action == "reply":
            result = generate_reply(content)
            return {"result": result, "type": "reply"}
        else:
            raise HTTPException(status_code=400, detail="Invalid action.")
    title="AI Chat Assistant",
    description="Bot for summarizing chats, extracting tasks and generating replies"
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/summarize", response_model=AIResponse)
def summarize_text(req: TextRequest):
    result = summarize(req.text)
    return {"result": result, "type": "summary"}

@app.post("/tasks", response_model=AIResponse)
def tasks(req: TextRequest):
    result = extract_tasks(req.text)
    return {"result": result, "type": "tasks"}

@app.post("/reply", response_model=AIResponse)
def reply(req: TextRequest):
    result = generate_reply(req.text)
    return {"result": result, "type": "reply"}

@app.post("/chat")
def smart_router(req: TextRequest):
    text = req.text.lower()

    if "משימה" in text or "todo" in text:
        return {"result": extract_tasks(req.text), "type": "tasks"}

    if "סכם" in text:
        return {"result": summarize(req.text), "type": "summary"}

    return {"result": generate_reply(req.text), "type": "reply"}