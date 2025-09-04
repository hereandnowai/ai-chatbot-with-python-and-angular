#!/usr/bin/env python3

from chatbot import chatbot
import tempfile
import os

# Test 1: Text-only chat
print("=== Test 1: Text-only chat ===")
result = chatbot("Hello, tell me about Angular signals")
print(f"Result: {result[:100]}...")

# Test 2: Document chat
print("\n=== Test 2: Document chat ===")
test_content = """Test Document for Analysis

This document contains the following key features:
1. Document parsing capabilities
2. POML-based prompt orchestration
3. LLM integration for Retrieval-Augmented Generation (RAG)  
4. Support for multiple file formats (.pdf, .txt, .docx, .csv)

The system allows users to upload documents and ask questions about their content.
"""

# Create a temporary file
with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write(test_content)
    temp_path = f.name

try:
    print(f"Temp file created: {temp_path}")
    print(f"File exists: {os.path.exists(temp_path)}")
    
    # Read file content to verify
    with open(temp_path, 'r') as f:
        content = f.read()
        print(f"File content length: {len(content)}")
        print(f"First 100 chars: {content[:100]}")
    
    # Test with chatbot
    result = chatbot("What are the key features mentioned in this document?", temp_path)
    print(f"Chatbot result: {result}")
    
finally:
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)
        print(f"Cleaned up temp file")
