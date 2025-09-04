from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile, os
from chatbot import chatbot

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    return {"response": chatbot(request.message)}

@app.post("/api/chat/upload")
async def upload_chat(file: UploadFile = File(), message: str = Form()):
    filename = file.filename or ""
    if not filename.endswith(('.pdf', '.txt', '.docx', '.csv')):
        raise HTTPException(400, "Invalid file type")
    
    # Get proper file extension
    import os
    _, ext = os.path.splitext(filename)
    
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix=ext) as temp:
        content = await file.read()
        temp.write(content)
        temp.flush()
        temp_path = temp.name
    
    try:
        response = chatbot(message, temp_path)
        return {"success": True, "message": response}
    finally:
        os.unlink(temp_path)

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, port=8001)