# AI Chatbot with POML Integration - Learning Project

## Overview
This project demonstrates how to build a modern AI chatbot with file upload capabilities using POML (Prompt Orchestration Markup Language) for prompt engineering. It's designed as a learning resource for beginners to understand prompt engineering concepts and POML integration.

## Key Features
- **Text Chat**: Simple conversational AI using POML templates
- **Document Analysis**: Upload and analyze PDF, TXT, DOCX, and CSV files
- **Angular Frontend**: Modern Angular v20+ with signals and standalone components
- **POML Integration**: Native document parsing without custom file parsing logic

## Architecture

### Backend (Python FastAPI)
- **api.py** - Simplified FastAPI application with two main endpoints:
  - `/api/chat` - Text-only conversations
  - `/api/chat/upload` - File upload and analysis
- **chatbot.py** - Core chatbot logic using POML templates
- **prompt.poml** - POML template for text conversations
- **document_prompt.poml** - POML template for document analysis

### Frontend (Angular)
- Modern Angular v20+ application with standalone components
- Drag-and-drop file upload interface
- Real-time chat interface

## POML Integration Benefits

### Before (Complex Approach)
- Custom file parsing logic for each format (PDF, DOCX, TXT, CSV)
- Manual content extraction and formatting
- ~300+ lines of parsing code in `file_parser.py`
- Error-prone file handling

### After (POML Native Approach)
- POML handles document parsing automatically with `<document src="{{ file_path }}" />`
- Automatic format detection and parsing
- Clean, readable templates
- ~60 lines of simplified code

## Key Learning Points

### 1. POML Document Handling
```xml
<document src="{{ file_path }}" />
```
- Automatically parses PDF, TXT, DOCX, CSV files
- No custom parsing logic needed
- Built-in error handling

### 2. Template Structure
```xml
<poml>
    <system-msg>
        <!-- System instructions -->
    </system-msg>
    
    <human-msg>
        <cp caption="Document to Analyze">
            <document src="{{ file_path }}" />
        </cp>
        
        <cp caption="User Question">
            <p>{{ question }}</p>
        </cp>
    </human-msg>
</poml>
```

### 3. List and Item Components
Using semantic markup for better organization:
```xml
<list listStyle="decimal">
    <item>Always use standalone components over NgModules</item>
    <item>Use signals for state management</item>
    <item>Use new control flow (@if, @for, @switch)</item>
</list>
```

## API Endpoints

### POST /api/chat
Simple text chat
```json
{
    "message": "What is Angular?"
}
```

### POST /api/chat/upload
File upload and analysis
```bash
curl -X POST "http://localhost:8002/api/chat/upload" \
  -F "file=@document.pdf" \
  -F "message=Summarize this document"
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY
   ```

3. **Start Backend**
   ```bash
   python3 -m uvicorn api:app --reload --host 0.0.0.0 --port 8002
   ```

4. **Start Frontend**
   ```bash
   cd frontend/chat-interface
   npm install
   npm start
   ```

## Educational Value

This project teaches:
- **Prompt Engineering**: How to structure prompts using POML
- **Document Processing**: Native POML document handling vs custom parsing
- **API Design**: Clean, simple FastAPI endpoints
- **Modern Frontend**: Angular v20+ best practices
- **File Handling**: Secure file upload and processing

## POML Benefits Demonstrated

1. **Simplicity**: Reduced codebase by 80%
2. **Reliability**: Built-in error handling and parsing
3. **Maintainability**: Clear, semantic templates
4. **Extensibility**: Easy to add new document types
5. **Best Practices**: Structured prompt engineering

## Next Steps for Learners

1. Experiment with different POML components
2. Add new document types
3. Implement structured output parsing
4. Add authentication and file management
5. Explore advanced POML features like tool calling

## Files Structure
```
├── api.py                  # FastAPI backend (simplified)
├── chatbot.py             # Core chatbot logic
├── prompt.poml            # Text chat template
├── document_prompt.poml   # Document analysis template
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── frontend/
    └── chat-interface/    # Angular application
```

This project demonstrates that with POML, you can build powerful AI applications with minimal code while maintaining clean, readable prompt templates that are easy to understand and modify.
