from keybert import KeyBERT
from transformers import AutoModel, AutoTokenizer

# Load model Bahasa Indonesia
model = AutoModel.from_pretrained("indobenchmark/indobert-base-p1")
tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p1")
kw_model = KeyBERT(model=model, tokenizer=tokenizer)

def extract_topic(text):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 1),
        stop_words=None,
        top_n=3
    )
    return [keyword[0] for keyword in keywords]