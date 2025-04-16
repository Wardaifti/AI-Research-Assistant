import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def fetch_core_papers(query, max_results=3):
    api_key = os.getenv("CORE_API_KEY")
    if not api_key:
        return [{"title": "Missing CORE_API_KEY", "source": "CORE"}]

    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"https://core.ac.uk:443/api-v2/search/{query}?page=1&pageSize={max_results}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return [{"title": f"CORE API error: {response.status_code}", "source": "CORE"}]

        data = response.json()
        papers = []

        for item in data.get("data", []):
            papers.append({
                "title": item.get("title", "N/A"),
                "authors": "N/A",  # CORE rarely returns authors
                "publication": item.get("publisher", "N/A"),
                "summary": item.get("description", "Summary not available"),
                "link": item.get("downloadUrl") or item.get("fullTextIdentifier", "N/A"),
                "source": "CORE"
            })

        return papers

    except Exception as e:
        return [{"title": f"CORE Exception: {str(e)}", "source": "CORE"}]

# Testing from terminal
if __name__ == "__main__":
    topic = input("Enter research topic: ")
    results = fetch_core_papers(topic)
    for i, paper in enumerate(results):
        print(f"\n[{i+1}] {paper['title']}")
        print(f"Summary: {paper['summary'][:300]}...")
        print(f"Link: {paper['link']}")
