from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.alert import AlertResponse, AlertStatusUpdate
from app.services.alert_service import list_alerts, update_alert_status, get_stats

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def list_alerts_endpoint(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await list_alerts(db, user_id)


@router.get("/stats")
async def alerts_stats(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await get_stats(db, user_id)


@router.patch("/{alert_id}/status", response_model=AlertResponse)
async def update_alert_status_endpoint(
    alert_id: str,
    data: AlertStatusUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await update_alert_status(db, alert_id, user_id, data.status)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return result
