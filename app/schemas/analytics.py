from pydantic import BaseModel
from typing import List, Dict, Any

class AnalyticsRequest(BaseModel):
    document_id: int

class AnomalyRequest(BaseModel):
    values: List[float]

class AnalyticsResponse(BaseModel):
    summary_stats: Dict[str, Any]
    insights: str

class AnomalyResponse(BaseModel):
    anomalies_detected: List[int]
    scores: List[float]