from crewai import Crew, Process
from tasks import research_task, financial_task, recommendation_task
from agents import research_analyst, financial_analyst, investment_advisor

crew = Crew(
    agents=[research_analyst, financial_analyst, investment_advisor],
    tasks=[research_task, financial_task, recommendation_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100
)

inputs = {"ticker": "AAPL"}
results = crew.kickoff(inputs=inputs)
print(results)
