import os
from crewai import LLM
from crewai import Agent
from tools.search_tools import search_internet
from tools.browser_tools import scrape_and_summarize_website

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.5,
    max_tokens=512,
    api_key="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",
    base_url=GROQ_API_KEY
)

research_analyst = Agent(
        role='The Best Research Analyst',
        goal="""Amaze all customers by being the best at gathering and interpreting data for ticker {ticker}""",
        backstory="""Known as the best research analyst, you're skilled in sifting through news, company announcements, and market sentiments working for a super important customer""",
        verbose=True,
        tools=[
            scrape_and_summarize_website,
            search_internet,
        ],
        llm=llm,
        allow_delegation=False
    )

research_analyst = Agent(
    role="The Best Research Analyst",
    goal="""Amaze all customers by being the best at gathering and interpreting data for ticker {ticker}.""",
    backstory="""Known as the best research analyst, you're skilled in sifting through news, company announcements, and market sentiments working for a super important customer.""",
    verbose=True,
    tools=[scrape_and_summarize_website, search_internet],
    llm=llm,
    allow_delegation=False,
)

financial_analyst = Agent(
        role='The Best Financial Analyst',
        goal="""Impress all customers with your financial data and market trends analysis for ticker {ticker}""",
        backstory="""The most seasoned financial analyst with lots of expertise in stock market analysis and investment strategies that is working for a super important customer.""",
        verbose=True,
        tools=[
            scrape_and_summarize_website,
            search_internet,
        ],
        llm=llm,
        allow_delegation=False
    )

investment_advisor = Agent(
        role='The Best Investment Advisor',
        goal="""Provide personalized investment advice based on the stock analysis report from the research and financial analysis.""",
        backstory="""As the best investment advisor, you are skilled at reviewing stock performance data and financial reports. You synthesize market news, company performance, and financial health to offer actionable investment advice.""",
        verbose=True,
        tools=[
            scrape_and_summarize_website,
            search_internet,
        ],
        llm=llm,
        allow_delegation=False
    )
