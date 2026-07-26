from functools import lru_cache
from typing import Dict, List

from transformers import pipeline


def normalize_label(label: str) -> str:
    """Normalize common sentiment labels to positive, neutral, or negative."""
    normalized = str(label).strip().lower()

    if normalized in {"positive", "pos", "label_2", "2"}:
        return "positive"
    if normalized in {"neutral", "neu", "neut", "label_1", "1"}:
        return "neutral"
    if normalized in {"negative", "neg", "label_0", "0"}:
        return "negative"

    return normalized


@lru_cache(maxsize=1)
def load_sentiment_model():
    """Load a three-class sentiment model once and reuse it."""
    return pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    )


def analyze_sentiment(text: str) -> Dict[str, float | str]:
    """Return sentiment label and confidence score for a single review."""
    classifier = load_sentiment_model()
    result = classifier(text)[0]

    label = normalize_label(result["label"])
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
            "label": normalize_label(result["label"]),
            "confidence": round(result["score"] * 100, 1),
        }
        for result in results
    ]
