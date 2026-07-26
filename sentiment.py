from functools import lru_cache
from typing import Dict, List

from transformers import pipeline


@lru_cache(maxsize=1)
def load_sentiment_model():
    """Load the pretrained Hugging Face sentiment-analysis model once and reuse it."""
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
    )


def analyze_sentiment(text: str) -> Dict[str, float | str]:
    """Return sentiment label and confidence score for a single review."""
    classifier = load_sentiment_model()
    result = classifier(text)[0]

    label = result["label"]
    score = round(result["score"] * 100, 1)

    return {
        "label": label,
        "confidence": score,
    }


def analyze_sentiment_batch(reviews: List[str]) -> List[Dict[str, float | str]]:
    """Analyze a list of reviews and return prediction results for each one."""
    classifier = load_sentiment_model()
    results = classifier(reviews)

    return [
        {
            "label": result["label"],
            "confidence": round(result["score"] * 100, 1),
        }
        for result in results
    ]
