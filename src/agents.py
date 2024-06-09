from crewai import Agent
from langchain_community.tools import DuckDuckGoSearchRun
from src.utils import fetch_pdf_content_from_url
from src.llms import openai_llm, gemini_llm, groq_llm
from langchain.tools import tool

llm = openai_llm()

@tool('DuckDuckGoSearch')
def search_tool(search_query: str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(search_query)

report_analyser = Agent(
            role="Senior health analyst",
            goal="Monitor and analyze health data"
                 "to identify any abnormalities, health issue and provide analysis.",
            backstory="Equipped with a deep understanding of health"
              "conditions and quantitative analysis, this agent "
              "devises and refines health strategies. It evaluates "
              "the performance of different approaches to determine "
              "the most optimal solution and risk-free options.",
            verbose=True,
            llm=llm,
            tools=[fetch_pdf_content_from_url("uploads/blood_test_report.pdf")]
        )

researcher = Agent(
    role="Senior health researcher",
    goal="Search over the internet for finding relevant articles based on user health condition",
    backstory="As a senior health researcher, you need to navigate and extract articles matching the health report. Your skills helps in pin pointing the neccessary and effective measure that can be taken",
    tools=[search_tool],
    verbose=True,
    llm=llm
)

recommender = Agent(
    role="Senior health consultant",
    goal="Provide necessary health recommendations based on user health condition",
    backstory="Provide most upto date health recommendations which will help in improving the lifestyle of the person and help in combating diseases",
    tools=[search_tool],
    verbose=True,
    llm=llm
)