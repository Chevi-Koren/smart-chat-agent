from fastapi import FastAPI, HTTPException
from schemas import TextRequest, AIResponse
from ai_service import summarize, extract_tasks, generate_reply
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
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