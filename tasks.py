import os
from crewai import Task
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from agents import financial_analyst, research_analyst, investment_advisor

from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
llm = ChatGroq(model="Gemma-7b-It", api_key=GROQ_API_KEY)

def extract_top_link(search_results):
    lines = search_results.split("\n")

    for line in lines:
        if "Link:" in line:
            return line.replace("Link: ", "").strip()
    return None

def execute_research(ticker):
    search_results = research_analyst.invoke_tool("Search topic on the internet", query=f"Latest news about {ticker}")
    top_link = extract_top_link(search_results)
    summary = research_analyst.invoke_tool("Scrape website content", website=top_link)
    
    return f"""
    Report for {ticker}:
    - Latest News: {search_results}
    - Summary of Top Article: {summary}
    """

def execute_financial_analysis(ticker):
    search_results = financial_analyst.invoke_tool("Search topic on the internet", query=f"Latest financial analysis of {ticker}")
    top_link = extract_top_link(search_results)
    summary = financial_analyst.invoke_tool("Scrape website content", website=top_link)

    return f"""
    Report for {ticker}:
    - Latest Financial News: {search_results}
    - Summary of Top Article: {summary}
    """

def execute_investment_advice(financial_summary, research_summary, llm):

    combined_input = f"""
    Below are the summaries for the stock under consideration:
    
    Financial Summary:
    {financial_summary}
    
    Research Summary:
    {research_summary}
    
    Based on the above information, provide a detailed recommendation about whether to buy, hold, or sell the stock.
    Include key justifications for your recommendation, considering the financial health and market sentiments.
    """
    
    prompt = PromptTemplate(
        input_variables=["combined_input"],
        template="{combined_input}"
    )

    recommendation_chain = LLMChain(llm=llm, prompt=prompt)
    recommendation = recommendation_chain.run({"combined_input": combined_input})
    return recommendation

research_task = Task(
    description=("""Collect and summarize recent news articles and press releases for {ticker}.
    
    Subtasks:
    1. Use `search_internet` to find relevant news articles and press releases about {ticker}.
    2. Use `scrape_and_summarize_website` to extract and summarize content from the most relevant links.
    
    Combine all findings into a single report that includes:
    - A summary of the latest news and market sentiment
    - Key events impacting the stock
    - Any upcoming announcements or trends
    - The stock ticker ({ticker})
    
    Your output should be concise but include all key points, using the most recent and relevant data available.
    """),
    agent=research_analyst,
    expected_output="A comprehensive summary report of the latest news, market sentiment shifts, and potential impacts on the stock.",
    function=execute_research
)

financial_task = Task(
    description=("""Collect and summarize recent financial news articles for press releases for {ticker}.
    
    Subtasks:
    1. Use `search_internet` to find relevant financial news articles and press releases about {ticker}.
    2. Use `scrape_and_summarize_website` to extract and summarize content from the most relevant links.
    
    Combine all findings into a single report that includes:
    - A summary of the latest financial news and market sentiment
    - Key events impacting the stock
    - Any upcoming announcements or trends
    - The stock ticker ({ticker})
    
    Your output should be concise but include all key points, using the most recent and relevant data available.
    """),
      agent=financial_analyst,
      expected_output="A detailed financial analysis report including key financial metrics and a comparison with industry peers.",
      function=execute_financial_analysis
    )

recommendation_task = Task(
    description="""Based on the research and financial analysis, provide a recommendation on the stock. 
    This recommendation should include:
    - A synthesis of the latest research findings and news.
    - An evaluation of the financial health of the stock.
    - A final recommendation: 'Buy', 'Sell', or 'Hold' based on the data.
    
    Ensure your recommendation aligns with the stock's performance, both in terms of market sentiment and financial stability.""",
    agent=investment_advisor,
    expected_output="A clear investment recommendation (Buy, Sell, Hold) with supporting reasons based on both research and financial analysis.",
    function=lambda inputs: execute_investment_advice(inputs.get("research"), inputs.get("financial_analysis"))
)