import os
from crewai import Agent
from tools.search_tools import SearchTools
from tools.browser_tools import ScrapingAnt
from tools.calculator_tools import CalculatorTools
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_community.tools import YahooFinanceNewsTool

from dotenv import load_dotenv
load_dotenv()

llm=ChatNVIDIA(model="meta/llama3-70b-instruct")

class StockAnalysisAgents(object):
    def financial_analyst(self):
        return Agent(
            role='The Best Financial Analyst',
            goal="""Impress all customers with your financial data and market trends analysis""",
            backstory="""The most seasoned financial analyst with lots of expertise in stock market analysis and investment
                         strategies that is working for a super important customer.""",
            verbose=True,
            tools=[
                ScrapingAnt.scrape_and_summarize_website,
                SearchTools.search_internet,
                CalculatorTools.calculate,
            ],
            llm=llm,
            allow_delegation=True
        )

    def research_analyst(self):
        return Agent(
            role='The Best Research Analyst',
            goal="""Amaze all customers by being the best at gathering and interpreting data""",
            backstory="""Known as the best research analyst, you're skilled in sifting through news, company announcements, 
                         and market sentiments working for a super important customer""",
            verbose=True,
            tools=[
                ScrapingAnt.scrape_and_summarize_website,
                SearchTools.search_internet,
                SearchTools.search_news,
                YahooFinanceNewsTool()
            ],
            llm=llm,
            allow_delegation=True
        )

    def investment_advisor(self):
        return Agent(
            role='The Best Investment Advisor',
            goal="""Impress your customers with thorough analyses of stocks and complete investment recommendations""",
            backstory="""As the most experienced investment advisor, combine various analytical insights to formulate
                         strategic investment advice. You are now working for a super important customer you need to impress.""",
            verbose=True,
            tools=[
                ScrapingAnt.scrape_and_summarize_website,
                SearchTools.search_internet,
                SearchTools.search_news,
                CalculatorTools.calculate,
                YahooFinanceNewsTool()
            ],
            llm=llm,
            allow_delegation=True
        )