import os
from crewai import Agent
from crewai import LLM
from tools.search_tools import SearchTools
from tools.browser_tools import ScrapingAnt
from tools.calculator_tools import CalculatorTools
from langchain_community.tools import YahooFinanceNewsTool

from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model="groq/llama3-8b-8192",
    temperature=0.5,
    max_tokens=512,
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

class YahooFinanceNewsWrapper:
    def __init__(self):
        self.yahoo_tool = YahooFinanceNewsTool()
        self.name = "yahoo_finance_news"
        self.description = "Fetches financial news about a public company. Input should be a company ticker (eg 'AAPL')."
        self.args = ["ticker"]

    def __call__(self, ticker="AAPL"):
        """
        A callable wrapper for YahooFinanceNewsTool to ensure a string input.
        """
        if not isinstance(ticker, str):
            raise ValueError("Ticker must be a string representing the company symbol.")
        return self.yahoo_tool(ticker)

class StockAnalysisAgents(object):

    def __init__(self):
        self.yahoo_finance_news_tool = YahooFinanceNewsWrapper()

    def yahoo_finance_news_wrapper(self, ticker="AAPL"):
        """
        A wrapper function for YahooFinanceNewsTool to ensure a string input.
        """
        if not isinstance(ticker, str):
            raise ValueError("Ticker must be a string representing the company symbol.")
        
        yahoo_tool = YahooFinanceNewsTool()
        news_summary = yahoo_tool(query=ticker)
        return news_summary

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
                self.yahoo_finance_news_tool
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
                self.yahoo_finance_news_tool
            ],
            llm=llm,
            allow_delegation=True
        )