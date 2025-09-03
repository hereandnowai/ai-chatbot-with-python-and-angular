import os
from dotenv import load_dotenv
from poml.integration.langchain import LangchainPomlTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=os.getenv("GEMINI_API_KEY"))

def chatbot(user_input):
    prompt_template = LangchainPomlTemplate.from_file("prompt.poml")
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"question": user_input})

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        response = chatbot(user_input)
        print("Caramel AI:", response)