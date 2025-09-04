from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException
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
    allow_origins=["*"],   # You can restrict this later to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body structure
class ChatRequest(BaseModel):
    message: str

class FileUploadResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    file_id: Optional[str] = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    bot_response = chatbot(user_message)
    return {"response": bot_response}

@app.post("/api/chat/upload", response_model=FileUploadResponse)
async def upload_file_and_chat(
    file: UploadFile = File(...),
    message: str = Form(...)
):
    """
    Handle file upload and process it with the chatbot.
    Supports PDF, TXT, DOCX, and CSV files.
    """
    
    # Check file type
    allowed_extensions = {'.pdf', '.txt', '.docx', '.csv'}
    filename = file.filename or "unknown"
    file_extension = Path(filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Check file size (limit to 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum size is 10MB."
        )
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Process file with chatbot
        bot_response = chatbot_with_document(temp_file_path, message)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        return {
            "success": True,
            "message": bot_response,
            "filename": file.filename
        }
        
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
