from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")


def is_sentiment(text):
    pipe = pipeline(
        "text-classification",
        model="ayameRushia/roberta-base-indonesian-1.5G-sentiment-analysis-smsa"
    )

    result = pipe(text)
    return result[0]["label"].lower()
