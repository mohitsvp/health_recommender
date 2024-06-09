from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

def groq_llm():
    return ChatGroq(
        model="mixtral-8x7b-32768",
        verbose=True,
        temperature=0.5
    )


def gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        verbose=True,
        temperature=0.5,
    )

def openai_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        verbose=True,
        temperature=0.5,
    )