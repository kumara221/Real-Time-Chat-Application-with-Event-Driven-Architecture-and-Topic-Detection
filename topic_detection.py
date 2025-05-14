from keybert import KeyBERT

# Inisialisasi model KeyBERT dengan IndoBERT
kw_model = KeyBERT(model="indobenchmark/indobert-base-p1")

def extract_topic(text):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 1), 
        stop_words=None,               
        top_n=3                       
    )
    return [keyword[0] for keyword in keywords]
