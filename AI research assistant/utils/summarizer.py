from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summarize_text_textrank(text, sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, sentences)
    
    return " ".join(str(sentence) for sentence in summary)

# Optional: test when run directly
if __name__ == "__main__":
    sample_text = """Natural Language Processing (NLP) is a field of artificial intelligence that gives machines the ability to read, understand, and derive meaning from human languages. It is a field that is growing rapidly in both research and industry applications."""
    print(summarize_text_textrank(sample_text, sentences=2))
