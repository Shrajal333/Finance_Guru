import pdfkit
import streamlit as st
from crewai import Crew
from tasks import StockAnalysisTasks
from agents import StockAnalysisAgents

from dotenv import load_dotenv
load_dotenv()

class FinancialCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        try:
            agents = StockAnalysisAgents()
            tasks = StockAnalysisTasks()

            research_analyst_agent = agents.research_analyst()
            financial_analyst_agent = agents.financial_analyst()
            investment_advisor_agent = agents.investment_advisor()

            research_task = tasks.research(research_analyst_agent, self.company)
            financial_task = tasks.financial_analysis(financial_analyst_agent)
            recommend_task = tasks.recommend(investment_advisor_agent)

            crew = Crew(
                agents=[
                    research_analyst_agent,
                    financial_analyst_agent,
                    investment_advisor_agent
                ],
                tasks=[
                    research_task,
                    financial_task,
                    recommend_task
                ],
                verbose=True
            )

            result = crew.kickoff()
            return result
        
        except Exception as e:
            return f"Error in processing: {e}"

def main():
    st.title("MultiAgent Finance Consultant🔍")
    company = st.text_input(
        "**Enter the company name you want to research and analyze:**",
        help='This FinAI Consultant analyzes financial data, researches market trends, and provides investment recommendations using an advanced multi-agent system.'
    )

    st.sidebar.header(":orange[MultiAgent Finance Consultant]")
    st.sidebar.caption("""
        Leverage a multi-agent system with a **Research Analyst, Financial Analyst, and Investment Advisor** to derive strategic investment plans. Enter the stock ticker of any listed company, and let our virtual experts collaborate to provide well-informed investment decisions.
    """)

    # Sidebar with additional guidance and information
    st.sidebar.subheader("How to Use:")
    st.sidebar.caption("""
        1. **:orange[Enter Stock Ticker]**: Provide the ticker symbol of a listed company (e.g., AAPL for Apple Inc.).
        2. **:orange[Submit]**: Click the "Analyze" button to start the analysis.
    """)
    
    st.sidebar.subheader("Disclaimer:")
    st.sidebar.caption("""
        - **:orange[Risk Notice]**: :red[Investments are subject to market risks]. FinAgents Suite provides insights based on available data, but it does not guarantee returns. Consult a financial advisor before making investment decisions.
    """)

    if st.button("Analyze and Generate Report"):
        if company:
            financial_crew = FinancialCrew(company)
            result = financial_crew.run()
            
            if "Error" in result:
                st.error(result)
            else:
                st.markdown("## Investment Recommendations")
                st.markdown(result)
                
                if st.button("Download Report as PDF"):
                    try:
                        pdf = pdfkit.from_string(result, False)
                        st.download_button("Download PDF", pdf, company + "_report.pdf", "application/pdf")
                    except Exception as e:
                        st.error("PDF generation failed. Ensure wkhtmltopdf is installed.")
        else:
            st.error("Please enter a company name to analyze.")

if __name__ == "__main__":
    main()