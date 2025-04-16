import requests

# Extract full abstract text from OpenAlex's inverted index format
def extract_abstract_text(inverted_index):
    if isinstance(inverted_index, dict):
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort()
        words = [word for _, word in word_positions]
        return " ".join(words)
    return "Summary not available"

# Fetch papers from OpenAlex based on a query
def fetch_openalex_papers(query, max_results=3):
    url = f"https://api.openalex.org/works?filter=title.search:{query}&per-page={max_results}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)

        data = response.json()
        papers = []

        for item in data.get("results", []):
            abstract_text = extract_abstract_text(item.get("abstract_inverted_index"))
            authors = ", ".join(
                [author["author"]["display_name"] for author in item.get("authorships", [])]
            ) or "N/A"

            papers.append({
                "title": item.get("title", "N/A"),
                "authors": authors,
                "publication": item.get("host_venue", {}).get("display_name", "N/A"),
                "summary": abstract_text,
                "link": item.get("doi", "N/A"),
                "source": "OpenAlex"
            })

        return papers

    except requests.exceptions.RequestException as e:
        return [{
            "title": f"OpenAlex API error: {str(e)}",
            "source": "OpenAlex",
            "summary": "",
            "authors": "N/A",
            "publication": "N/A",
            "link": ""
        }]
