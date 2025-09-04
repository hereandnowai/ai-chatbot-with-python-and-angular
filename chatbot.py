import os
from dotenv import load_dotenv
from poml.integration.langchain import LangchainPomlTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=os.getenv("GEMINI_API_KEY"))

def chatbot(user_input):
    """Simple text-only chatbot using POML prompt template."""
    prompt_template = LangchainPomlTemplate.from_file("prompt.poml")
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"question": user_input})

def chatbot_with_document(file_path: str, user_query: str):
    """
    Enhanced chatbot that processes documents using POML's native document handling.
    POML automatically handles PDF, TXT, DOCX, and CSV parsing.
    """
    try:
        # Use POML template with document handling
        prompt_template = LangchainPomlTemplate.from_file("document_prompt.poml")
        chain = prompt_template | llm | StrOutputParser()
        
        # Pass file path and question to POML template
        response = chain.invoke({
            "file_path": file_path,
            "question": user_query
        })
        
        return response
        
    except Exception as e:
        return f"Error processing document: {str(e)}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        response = chatbot(user_input)
        print("Caramel AI:", response)