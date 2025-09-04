import os
from dotenv import load_dotenv
from poml.integration.langchain import LangchainPomlTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from file_parser import FileParser, PomlDocumentRenderer

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=os.getenv("GEMINI_API_KEY"))

def chatbot(user_input):
    """Standard chatbot function for text-only conversations."""
    prompt_template = LangchainPomlTemplate.from_file("prompt.poml")
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"question": user_input})

def chatbot_with_document(file_path: str, user_query: str):
    """
    Enhanced chatbot function that processes uploaded documents using POML.
    
    Args:
        file_path: Path to the uploaded file
        user_query: User's question about the document
        
    Returns:
        AI response incorporating document analysis
    """
    try:
        # Parse the file
        file_content = FileParser.parse_file(file_path)
        
        if not file_content.get('parsed_successfully'):
            return f"Sorry, I couldn't parse the file: {file_content.get('content', 'Unknown error')}"
        
        # Create POML prompt with document content
        poml_prompt = PomlDocumentRenderer.render_document_with_poml(file_content, user_query)
        
        # Use the LLM to process the document
        response = llm.invoke(poml_prompt)
        
        # Extract the content from the response
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
            
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