import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.model import sentiment_model
from app.schemas import HealthResponse, PredictRequest, PredictResponse, ReadyResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Starting up — loading ML model...")
    sentiment_model.load()
    logger.info("Model ready.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="Sentiment Analysis API",
    description="A simple ML-powered sentiment analysis service.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Liveness probe — returns 200 if the server process is running."""
    return HealthResponse(status="ok")


@app.get("/ready", response_model=ReadyResponse)
async def ready():
    """Readiness probe — returns 200 only when the model is loaded and ready to serve."""
    if not sentiment_model.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    return ReadyResponse(status="ready", model_loaded=True)


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """Run sentiment analysis on the provided text."""
    if not sentiment_model.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    sentiment, confidence = sentiment_model.predict(request.text)
    return PredictResponse(sentiment=sentiment, confidence=confidence)
