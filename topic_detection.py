from keybert import KeyBERT
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Inisialisasi model KeyBERT dengan IndoBERT
kw_model = KeyBERT(model="indobenchmark/indobert-base-p1")

# Inisialisasi Stopword Remover dan Stemmer
stopword_factory = StopWordRemoverFactory()
stopword_remover = stopword_factory.create_stop_word_remover()

stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

def preprocess_text(text):
    text = text.lower()
    text = stopword_remover.remove(text)
    text = stemmer.stem(text)
    return text

def extract_topic(text):
    preprocessed_text = preprocess_text(text)

    print("Kalimat setelah preprocessing:")
    print(preprocessed_text)
    
    keywords = kw_model.extract_keywords(
        preprocessed_text,
        keyphrase_ngram_range=(1, 1), 
        stop_words=None,               
        top_n=3                        
    )
    return [keyword[0] for keyword in keywords]