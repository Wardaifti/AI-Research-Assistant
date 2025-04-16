# AI-Research-Assistant
A web app to search research papers from ArXiv, OpenAlex &amp; CORE, and summarize uploaded PDFs using AI. Built with Flask, HTML, and Python.
An AI-powered web application that helps students, researchers, and enthusiasts to:
- 🔍 Search research papers from ArXiv, OpenAlex, and CORE
- 📄 Upload academic documents (PDF/DOCX/TXT) and get summarized insights
Built with Python, Flask, and clean UI using HTML & CSS.

## 🚀 Features

- 🔎 Search scholarly papers using APIs (ArXiv, OpenAlex, CORE)
- 📂 Upload research papers in PDF, DOCX, or TXT formats
- 🧠 Get concise summaries using AI-powered TextRank
- 🎨 Responsive and minimal UI
- 🧰 Easy to customize or extend

  ## 🏗️ Directory Structure

ai-research-assistant/ │ ├── app.py # Main Flask app ├── requirements.txt # Python dependencies ├── .env # API keys (keep this secret) ├── README.md # Project info ├── templates/ │ ├── index.html # Home page │ ├── search.html # Paper search UI │ └── result.html # (optional) Summary results │ ├── static/ │ └── style.css # Custom styling │ ├── fetchers/ │ ├── arxiv_fetch.py # ArXiv API wrapper │ └── openalex_fetch.py # OpenAlex API wrapper │ ├── utils/ │ └── summarizer.py # File processing & summarization ├── uploads/ # Temporary uploaded files └── .gitignore # Files to ignore in Git


---

## 🛠️ Installation & Setup

### 1. Clone the repository

bash
git clone https://github.com/yourusername/ai-research-assistant.git
cd ai-research-assistant

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

pip install -r requirements.txt

CORE_API_KEY=your_core_api_key


 ### 📦 Dependencies
Flask
python-docx
pytesseract
PyMuPDF
PIL
requests
python-dotenv


 ## 🙌 Contribution
Pull requests and feedback are welcome!

 ## 📄 License
MIT License © 2025 [Warda]


Open issues for suggestions, bugs, or features.
