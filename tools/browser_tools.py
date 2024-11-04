import os
import json
import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

from dotenv import load_dotenv
load_dotenv()

class ScrapingAnt():

    @tool("Scrape website content")
    def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""

        url = f"https://api.scrapingant.com/v2/extended?url={website}&x-api-key={os.environ['SCRAPINGANT_API_KEY']}"
        payload = json.dumps({"url": website})

        headers = {'cache-control': 'no-cache', 
                   'content-type': 'application/json',
                   'User-Agent': os.environ['USER_AGENT']}

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve content: {response.status_code}")
        
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(element) for element in elements])
        content_chunks = [content[i:i + 8000] for i in range(0, len(content), 8000)]

        summaries = []
        for chunk in content_chunks:

            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing research and provide concise summary of the content',
                backstory="You're a Principal Researcher at a large company doing research about a given topic.",
                allow_delegation=False
            )
            
            task = Task(
                agent=agent,
                description=f'Analyze and summarize the content below. Make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
            )

            summary = task.execute()
            summaries.append(summary)

        return "\n\n".join(summaries)