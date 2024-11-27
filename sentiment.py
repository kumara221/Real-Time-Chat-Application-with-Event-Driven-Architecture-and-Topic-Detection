from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def is_sentiment(text):
    tokenizer = AutoTokenizer.from_pretrained(
        "ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa")
    model = AutoModelForSequenceClassification.from_pretrained(
        "ayameRushia/bert-base-indonesian-1.5G-sentiment-analysis-smsa")

    sentiment_analysis = pipeline(
        "sentiment-analysis", model=model, tokenizer=tokenizer)

    result = sentiment_analysis(text)
    return result[0]["label"].lower()
