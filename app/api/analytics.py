from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.analytics import AnalyticsRequest, AnomalyRequest, AnalyticsResponse, AnomalyResponse
from app.services.auth_service import get_current_user
from app.services.analytics_service import analyze_csv_document
from app.services.ml_service import detect_anomalies

router = APIRouter(prefix="/analytics", tags=["Analytics & ML"])

@router.post("/insights", response_model=AnalyticsResponse)
def get_business_insights(
    payload: AnalyticsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    owner_filter = None if current_user.is_superuser else current_user.id
    return analyze_csv_document(db, payload.document_id, owner_id=owner_filter)

@router.post("/detect-anomalies", response_model=AnomalyResponse)
def ml_detect_anomalies(
    payload: AnomalyRequest,
    current_user: User = Depends(get_current_user)
):
    return detect_anomalies(payload.values)