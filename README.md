# AI Chatbot with POML Integration

<div align="center">
  <img src="https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/logo-of-here-and-now-ai.png" alt="HERE AND NOW AI" width="200"/>
  
  **designed with passion for innovation**
  
  [![Website](https://img.shields.io/badge/Website-hereandnowai.com-blue)](https://hereandnowai.com)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-hereandnowai-blue)](https://www.linkedin.com/company/hereandnowai/)
  [![GitHub](https://img.shields.io/badge/GitHub-hereandnowai-black)](https://github.com/hereandnowai)
</div>

## 🚀 Overview

This project demonstrates how to build a modern AI chatbot with file upload capabilities using **POML (Prompt Orchestration Markup Language)** for advanced prompt engineering. Perfect for beginners learning AI development and prompt engineering concepts.

### 🎯 What You'll Learn
- Modern prompt engineering with POML
- FastAPI backend development
- Angular v20+ frontend with signals
- Document processing and analysis
- File upload handling
- AI integration best practices

## ✨ Key Features

- 💬 **Text Chat**: Conversational AI powered by POML templates
- 📄 **Document Analysis**: Upload and analyze PDF, TXT, DOCX, CSV files
- 🎨 **Modern UI**: Angular v20+ with signals and standalone components
- 🔄 **POML Integration**: Native document parsing without custom logic
- 🚀 **Simplified API**: Clean, beginner-friendly FastAPI endpoints

## 🏗️ Architecture

### Backend Stack
- **Python 3.10+** with FastAPI
- **POML** for prompt orchestration
- **Google Gemini AI** for language processing
- **Langchain** for AI framework integration

### Frontend Stack
- **Angular v20+** with signals
- **Standalone Components** architecture
- **Drag & Drop** file upload
- **Real-time** chat interface

## 📁 Project Structure

```
ai-chatbot-with-python-and-angular/
├── 🐍 Backend (Python FastAPI)
│   ├── api.py              # Main FastAPI application (30 lines!)
│   ├── chatbot.py          # Core chatbot logic
│   ├── prompt.poml         # POML template for chat & documents
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
│
├── 🅰️ Frontend (Angular)
│   └── chat-interface/
│       ├── src/app/
│       │   ├── components/chat/
│       │   └── services/
│       ├── public/
│       │   └── branding.json
│       └── package.json
│
└── 📚 Documentation
    └── README.md          # This file
```

## 🛠️ Complete Setup Guide

### Prerequisites

Before you start, ensure you have:
- **Node.js 18+** installed
- **Python 3.10+** installed
- **Git** installed
- **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/hereandnowai/ai-chatbot-with-python-and-angular.git

# Navigate to project directory
cd ai-chatbot-with-python-and-angular
```

### Step 2: Backend Setup (Python FastAPI)

#### 2.1 Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

#### 2.2 Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

#### 2.3 Environment Configuration

```bash
# Create environment file
cp .env.example .env

# Edit .env file and add your API key
nano .env
```

Add your Google Gemini API key to `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

#### 2.4 Start Backend Server

```bash
# Start the FastAPI server
python api.py

# Alternative: Use uvicorn directly
# uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

✅ **Backend Running**: http://localhost:8001

### Step 3: Frontend Setup (Angular)

Open a **new terminal** and navigate to the frontend directory:

#### 3.1 Install Angular Dependencies

```bash
# Navigate to frontend directory
cd frontend/chat-interface

# Install Node.js dependencies
npm install
```

#### 3.2 Start Frontend Development Server

```bash
# Start Angular development server
npm start

# Alternative command:
# ng serve
```

✅ **Frontend Running**: http://localhost:4200

## 🎮 Usage Guide

### Text Chat
1. Open http://localhost:4200
2. Type your question about Angular development
3. Press Send or hit Enter

**Example Questions:**
```
What are Angular signals?
How do I create standalone components?
Explain the new control flow syntax
```

### Document Analysis
1. Click the 📎 attachment icon
2. Upload a document (PDF, TXT, DOCX, CSV)
3. Ask questions about the document content

**Example Questions:**
```
What are the key features in this document?
Summarize the main points
What technologies are mentioned?
```

## 🔧 API Endpoints

### Health Check
```bash
GET http://localhost:8001/api/health
```

### Text Chat
```bash
POST http://localhost:8001/api/chat
Content-Type: application/json

{
    "message": "What is Angular?"
}
```

### File Upload & Analysis
```bash
POST http://localhost:8001/api/chat/upload
Content-Type: multipart/form-data

file: [your-document.pdf]
message: "Analyze this document"
```

## 💡 POML Magic Explained

### Before POML (Complex Way)
```python
# Custom file parsing - 300+ lines of code
if file.endswith('.pdf'):
    content = extract_pdf_text(file)
elif file.endswith('.docx'):
    content = extract_docx_text(file)
elif file.endswith('.txt'):
    content = read_text_file(file)
# ... more parsing logic
```

### After POML (Simple Way)
```xml
<!-- Just 1 line in POML template! -->
<document src="{{ file_path }}" parser="auto" />
```

### Complete POML Template
```xml
<poml>
    <system-msg>
        <p if="{{ file_path }}">Document analysis assistant</p>
        <p if="{{ !file_path }}">Angular development expert</p>
    </system-msg>
    
    <human-msg>
        <!-- Document content (if uploaded) -->
        <cp if="{{ file_path }}" caption="Document Content">
            <document src="{{ file_path }}" parser="auto" />
        </cp>
        
        <!-- User question -->
        <cp caption="User Question">
            <p>{{ question }}</p>
        </cp>
    </human-msg>
</poml>
```

## 🚀 Development Workflow

### For Backend Changes

1. **Modify Code**: Edit `api.py`, `chatbot.py`, or `prompt.poml`
2. **Auto-Reload**: FastAPI automatically reloads on changes
3. **Test**: Use curl or frontend to test changes

```bash
# Test text chat
curl -X POST "http://localhost:8001/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'

# Test file upload
curl -X POST "http://localhost:8001/api/chat/upload" \
  -F "file=@test.txt" \
  -F "message=Analyze this file"
```

### For Frontend Changes

1. **Modify Code**: Edit Angular components in `src/app/`
2. **Auto-Reload**: Angular CLI automatically reloads browser
3. **Test**: Interact with the chat interface

## 🎯 Key Learning Points

### 1. Simplified API Design
- **30 lines** of FastAPI code instead of 200+
- **2 endpoints** handle all functionality
- **Clean error handling** and file management

### 2. Modern Angular Practices
```typescript
// Using signals for reactive state
isConnected = signal<boolean>(false);

// Standalone components
@Component({
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})

// New control flow
@if (isConnected()) {
  <p>Backend connected ✅</p>
} @else {
  <p>Backend disconnected ❌</p>
}
```

### 3. POML Best Practices
- **Conditional logic** with `if="{{ condition }}"`
- **Semantic components** like `<cp>` and `<document>`
- **Template reuse** for multiple scenarios

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError`
```bash
# Solution: Activate virtual environment
source .venv/bin/activate
pip install -r requirements.txt
```

**Problem**: `GEMINI_API_KEY not found`
```bash
# Solution: Check .env file
cat .env
# Make sure GEMINI_API_KEY=your_key_here
```

**Problem**: Port 8001 already in use
```bash
# Solution: Kill existing process
pkill -f "python.*api.py"
# Or use different port
uvicorn api:app --port 8002
```

### Frontend Issues

**Problem**: `ng: command not found`
```bash
# Solution: Install Angular CLI
npm install -g @angular/cli
```

**Problem**: Port 4200 already in use
```bash
# Solution: Use different port
ng serve --port 4201
```

**Problem**: Backend connection failed
- ✅ Check backend is running on http://localhost:8001
- ✅ Check CORS is enabled in `api.py`
- ✅ Verify `/api/health` endpoint responds

## 📝 Example Use Cases

### 1. Learning Angular
```
User: "What are the benefits of signals in Angular?"
AI: "Signals provide fine-grained reactivity, better performance..."
```

### 2. Document Analysis
```
Upload: project-requirements.pdf
Question: "What are the main requirements?"
AI: "The document lists 5 key requirements: 1. User authentication..."
```

### 3. Code Review
```
Upload: component.ts
Question: "How can I improve this component?"
AI: "Consider using signals instead of observables for state management..."
```

## 🌟 Advanced Features

### Custom POML Templates

Create specialized templates for different use cases:

```xml
<!-- Code review template -->
<poml>
    <system-msg>
        <p>You are a senior Angular developer reviewing code for best practices.</p>
    </system-msg>
    
    <human-msg>
        <cp caption="Code to Review">
            <document src="{{ file_path }}" />
        </cp>
        
        <hint>Provide specific, actionable feedback using Angular v20+ best practices.</hint>
    </human-msg>
</poml>
```

### Environment Configurations

```bash
# Development
GEMINI_API_KEY=dev_key
DEBUG=true

# Production
GEMINI_API_KEY=prod_key
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

## 📞 Support & Contact

<div align="center">

**HERE AND NOW AI**

🌐 **Website**: [hereandnowai.com](https://hereandnowai.com)  
📧 **Email**: info@hereandnowai.com  
📱 **Mobile**: +91 996 296 1000  

**Connect with us:**
- 💼 [LinkedIn](https://www.linkedin.com/company/hereandnowai/)
- 📘 [Blog](https://hereandnowai.com/blog)
- 🐙 [GitHub](https://github.com/hereandnowai)
- 📸 [Instagram](https://instagram.com/hereandnow_ai)
- 🐦 [X (Twitter)](https://x.com/hereandnow_ai)
- 📺 [YouTube](https://youtube.com/@hereandnow_ai)

</div>

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <img src="https://raw.githubusercontent.com/hereandnowai/images/refs/heads/main/logos/caramel.jpeg" alt="Caramel AI" width="50"/>
  <br>
  <em>Built with ❤️ by HERE AND NOW AI</em>
  <br>
  <strong>designed with passion for innovation</strong>
</div>
