from crewai import Task
from src.agents import report_analyser,researcher, recommender

analyze_report = Task(
    description="Analyse the health report and prepare a detailed analysis on the health conditions"
        "your report should be highly detailed. providing a proper diagnosis and test results",
    expected_output=(
        "A detailed document provide complete analysis of health condition"
    ),
    agent=report_analyser,
    delegation=False,
    )


research_health = Task(
    description="Search for articles matchining health conditions of the report. Do end to end search on the user health condition",
    expected_output=(
        "A detailed list of articles with their summaries based on user health condition"
    ),
    agent=researcher,
    context=[analyze_report]
)


health_recommendations = Task(
    description="Providing health recommendations that will be helpful for improving the lifestyle and mitigating diseases. Make it as detailed as possible in a user friendly tone considering who is not from medical background. So the language should be very easy to understand",
    expected_output=(
        "A detailed health recommendation report based on health report providing diagnosis, mitigation and improving the lifestyle in point wise format like a lab report"),
        agent=recommender,
        output_file="healthReport.md"
    )
