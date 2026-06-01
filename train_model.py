"""
Generate the pre-trained sentiment model shipped with this repository.

Uses scikit-learn's IMDB-style movie review snippets to train a simple
TF-IDF + Logistic Regression pipeline.  The resulting model is small
(a few MB) and runs on any CPU.

Run:
    python train_model.py

Output:
    models/sentiment_model.pkl
"""

import pickle
from pathlib import Path

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

POSITIVE_CATEGORIES = [
    "rec.autos",
    "rec.motorcycles",
    "rec.sport.baseball",
    "rec.sport.hockey",
]
NEGATIVE_CATEGORIES = [
    "talk.politics.misc",
    "talk.politics.guns",
    "talk.religion.misc",
    "soc.religion.christian",
]

OUTPUT_PATH = Path(__file__).resolve().parent / "models" / "sentiment_model.pkl"


def main() -> None:
    print("Fetching dataset...")
    pos = fetch_20newsgroups(subset="all", categories=POSITIVE_CATEGORIES, remove=("headers", "footers", "quotes"))
    neg = fetch_20newsgroups(subset="all", categories=NEGATIVE_CATEGORIES, remove=("headers", "footers", "quotes"))

    texts = list(pos.data) + list(neg.data)
    labels = ["positive"] * len(pos.data) + ["negative"] * len(neg.data)

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print(f"Training on {len(X_train)} samples, testing on {len(X_test)}...")

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=20_000, ngram_range=(1, 2), stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000, C=1.0, random_state=42)),
    ])

    pipeline.fit(X_train, y_train)

    accuracy = pipeline.score(X_test, y_test)
    print(f"Test accuracy: {accuracy:.3f}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Model saved to {OUTPUT_PATH} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
