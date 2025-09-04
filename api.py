from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
from pathlib import Path
from typing import Optional
from chatbot import chatbot, chatbot_with_document

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class FileUploadResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Simple text chat endpoint."""
    return {"response": chatbot(request.message)}

@app.post("/api/chat/upload", response_model=FileUploadResponse)
async def upload_file_and_chat(
    file: UploadFile = File(...),
    message: str = Form(...)
):
    """
    Handle file upload and process it with POML.
    POML handles document parsing directly.
    """
    # Validate file type
    allowed_extensions = {'.pdf', '.txt', '.docx', '.csv'}
    filename = file.filename or "unknown"
    
    if Path(filename).suffix.lower() not in allowed_extensions:
        raise HTTPException(400, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        
        # Let POML handle document processing
        response = chatbot_with_document(temp_file_path, message)
        
        # Cleanup
        os.unlink(temp_file_path)
        
        return {
            "success": True,
            "message": response,
            "filename": file.filename
        }
        
    except Exception as e:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise HTTPException(500, f"Error processing file: {str(e)}")

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
