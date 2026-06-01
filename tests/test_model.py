import pytest

from app.model import SentimentModel


@pytest.fixture
def model():
    m = SentimentModel()
    m.load()
    return m


def test_model_loads_successfully(model):
    assert model.is_loaded


def test_predict_returns_sentiment_and_confidence(model):
    sentiment, confidence = model.predict("I love this product")
    assert sentiment in ("positive", "negative")
    assert isinstance(confidence, float)
    assert 0.0 <= confidence <= 1.0


def test_predict_positive_text(model):
    sentiment, confidence = model.predict(
        "This is the best thing ever, I am so happy and excited!"
    )
    assert sentiment == "positive"
    assert confidence > 0.5


def test_predict_negative_text(model):
    sentiment, confidence = model.predict(
        "The political situation is terrible and guns cause nothing but violence and death."
    )
    assert sentiment == "negative"
    assert confidence > 0.5


def test_predict_without_loading_raises():
    m = SentimentModel()
    with pytest.raises(RuntimeError, match="Model is not loaded"):
        m.predict("hello")
