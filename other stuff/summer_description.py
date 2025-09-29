from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import nltk
nltk.download('punkt')
text = """
Do Do Hee is the successor of the Future Group. She has an arrogant and cool-headed personality...
Jung Koo Won is a demon. He can live for eternity by making dangerous, but sweet deals with humans...
"""
# Step 1: Parse text
parser = PlaintextParser.from_string(text, Tokenizer("english"))

# Step 2: Create summarizer
summarizer = LexRankSummarizer()

# Step 3: Summarize: pick 2 sentences
summary = summarizer(parser.document, 3)

# Step 4: Print the summary
for sentence in summary:
    print(sentence)
