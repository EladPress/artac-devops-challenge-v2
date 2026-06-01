from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, examples=["This movie was fantastic!"])


class PredictResponse(BaseModel):
    sentiment: str = Field(..., examples=["positive"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.92])


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])


class ReadyResponse(BaseModel):
    status: str = Field(..., examples=["ready"])
    model_loaded: bool = Field(..., examples=[True])
