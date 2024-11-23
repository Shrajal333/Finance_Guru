import pdfkit
import streamlit as st
from crewai import Crew, Process
from tasks import research_task, financial_task, recommendation_task
from agents import research_analyst, financial_analyst, investment_advisor

from dotenv import load_dotenv
load_dotenv()

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
            crew = Crew(
                        agents=[research_analyst, financial_analyst, investment_advisor],
                        tasks=[research_task, financial_task, recommendation_task],
                        process=Process.sequential,
                        )
            
            inputs = {"ticker": company}
            results = crew.kickoff(inputs=inputs)

            if "Error" in results:
                st.error(results)
            else:
                st.markdown("## Investment Recommendations")
                st.markdown(results)
                
                if st.button("Download Report as PDF"):
                    try:
                        pdf = pdfkit.from_string(results, False)
                        st.download_button("Download PDF", pdf, company + "_report.pdf", "application/pdf")
                    except Exception as e:
                        st.error("PDF generation failed. Ensure wkhtmltopdf is installed.")
        else:
            st.error("Please enter a company name to analyze.")

if __name__ == "__main__":
    main()