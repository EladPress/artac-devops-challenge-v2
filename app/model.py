import logging
import pickle
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "sentiment_model.pkl"


class SentimentModel:
    """Lazy-loading wrapper around the pre-trained sentiment classifier."""

    def __init__(self) -> None:
        self._pipeline: Optional[object] = None

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None

    def load(self) -> None:
        if self._pipeline is not None:
            return
        logger.info("Loading model from %s ...", MODEL_PATH)
        with open(MODEL_PATH, "rb") as f:
            self._pipeline = pickle.load(f)
        logger.info("Model loaded successfully.")

    def predict(self, text: str) -> tuple[str, float]:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded. Call load() first.")

        probabilities = self._pipeline.predict_proba([text])[0]
        classes = self._pipeline.classes_

        predicted_idx = probabilities.argmax()
        sentiment = str(classes[predicted_idx])
        confidence = round(float(probabilities[predicted_idx]), 4)

        return sentiment, confidence


sentiment_model = SentimentModel()
