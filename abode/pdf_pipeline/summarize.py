from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

def summarize_section(text: str, sentences_count: int = 2) -> str:
    """
    Summarize a section using extractive TextRank summarization.
    Args:
        text (str): Section text to summarize.
        sentences_count (int): Number of sentences in summary.
    Returns:
        str: Extractive summary.
    """
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary_sentences = summarizer(parser.document, sentences_count)
    summary = " ".join(str(sentence) for sentence in summary_sentences)
    return summary 