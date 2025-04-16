from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF
import docx
import dotenv
import pytesseract
import requests
from PIL import Image
from urllib.parse import quote
from utils.summarizer import summarize_text_textrank
from fetchers.arxiv_fetch import fetch_arxiv_papers
from fetchers.openalex_fetch import fetch_openalex_papers, extract_abstract_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load environment variables
dotenv.load_dotenv()


# --------- Helper for OpenAlex Abstract ---------
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


# --------- File Processor ---------
def process_uploaded_file(file_path):
    ext = file_path.split('.')[-1].lower()

    if ext == "txt":
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif ext == "pdf":
        doc = fitz.open(file_path)
        text_list = []
        for page in doc:
            page_text = page.get_text("text")
            if not page_text.strip():
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_text = pytesseract.image_to_string(img)
            text_list.append(page_text)
        return "\n".join(text_list)

    elif ext == "docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    return None


# --------- OpenAlex API Fetch ---------
def fetch_openalex_papers(query, max_results=3):
    encoded_query = quote(query)
    url = f"https://api.openalex.org/works?filter=title.search:{encoded_query}&per-page={max_results}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("OpenAlex API Error:", response.status_code)
            return [{"title": "Error fetching OpenAlex papers", "source": "OpenAlex"}]

        data = response.json()
        papers = []
        for item in data.get("results", []):
            abstract_text = extract_abstract_text(item.get("abstract_inverted_index"))
            papers.append({
                "title": item.get("title", "N/A"),
                "authors": ", ".join([a["author"]["display_name"] for a in item.get("authorships", [])]) or "N/A",
                "publication": item.get("host_venue", {}).get("display_name", "N/A"),
                "summary": abstract_text,
                "link": item.get("doi", "N/A"),
                "source": "OpenAlex"
            })
        return papers

    except Exception as e:
        print("Exception in OpenAlex:", str(e))
        return [{"title": "Error fetching OpenAlex papers", "source": "OpenAlex"}]


# --------- CORE API Fetch ---------
def fetch_core_papers(query, max_results=3):
    CORE_API_KEY = os.getenv("CORE_API_KEY")
    if not CORE_API_KEY:
        print("CORE_API_KEY not found in .env")
        return [{"title": "Missing CORE API Key", "source": "CORE"}]

    url = f"https://core.ac.uk:443/api-v2/search/{quote(query)}?apiKey={CORE_API_KEY}"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("CORE API Error:", response.status_code)
            return [{"title": "Error fetching CORE papers", "source": "CORE"}]

        data = response.json()
        papers = []
        for item in data.get("data", [])[:max_results]:
            summary = item.get("description") or item.get("abstract") or "Summary not available"
            papers.append({
                "title": item.get("title", "N/A"),
                "authors": ", ".join(item.get("authors", [])) or "N/A",
                "summary": summary,
                "link": item.get("downloadUrl") or item.get("fullTextLink", "#"),
                "source": "CORE"
            })
        return papers

    except Exception as e:
        print("Exception in CORE:", str(e))
        return [{"title": "Error fetching CORE papers", "source": "CORE"}]


# --------- Homepage Route ---------
@app.route("/")
def index():
    return render_template("index.html")


# --------- Search Route ---------
@app.route("/search", methods=["GET", "POST"])
def search_papers():
    papers = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query")
        if query:
            arxiv_papers = fetch_arxiv_papers(query)
            openalex_papers = fetch_openalex_papers(query)
            core_papers = fetch_core_papers(query)

            for source_papers in [arxiv_papers, openalex_papers, core_papers]:
                if isinstance(source_papers, list):
                    papers.extend(source_papers)

            for paper in papers:
                paper.setdefault("summary", "Summary not available")

    return render_template("search.html", results=papers, query=query)


# --------- Run App ---------
if __name__ == "__main__":
    app.run(debug=True)
