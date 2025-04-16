import feedparser
import urllib.parse
from urllib import request

def fetch_arxiv_papers(query, max_results=5):
    """Fetches research papers from arXiv based on the given query using a custom user-agent."""
    base_url = "http://export.arxiv.org/api/query?search_query="
    query_encoded = urllib.parse.quote(query)
    search_url = f"{base_url}{query_encoded}&start=0&max_results={max_results}"

    try:
        # Use a custom user-agent to prevent being blocked
        req = request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0 (compatible; AIResearchBot/1.0)'})
        with request.urlopen(req) as response:
            data = response.read()

        feed = feedparser.parse(data)

        papers = []
        for entry in feed.entries:
            paper = {
                "title": entry.title,
                "authors": [author.name for author in entry.authors],
                "summary": entry.summary,
                "published": entry.published,
                "link": entry.link,
                "source": "arXiv"
            }
            papers.append(paper)

        return papers

    except Exception as e:
        print("❌ Error fetching from arXiv:", e)
        return []

# Testing from terminal
if __name__ == "__main__":
    query = input("Enter research topic: ")
    papers = fetch_arxiv_papers(query)
    if papers:
        for i, paper in enumerate(papers):
            print(f"\n[{i+1}] {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            print(f"Published: {paper['published']}")
            print(f"Summary: {paper['summary'][:300]}...")
            print(f"Link: {paper['link']}")
    else:
        print("No papers found or an error occurred.")
