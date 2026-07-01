from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.alert import Alert
from app.schemas.alert import AlertResponse


async def create_alert(db: AsyncSession, user_id: str, well_id: str, title: str, severity: str, description: str = "") -> AlertResponse:
    alert = Alert(
        user_id=user_id,
        well_id=well_id,
        title=title,
        severity=severity,
        description=description,
    )
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return AlertResponse.model_validate(alert)


async def list_alerts(db: AsyncSession, user_id: str) -> list[AlertResponse]:
    result = await db.execute(
        select(Alert).where(Alert.user_id == user_id).order_by(Alert.created_at.desc())
    )
    return [AlertResponse.model_validate(a) for a in result.scalars().all()]


async def update_alert_status(db: AsyncSession, alert_id: str, user_id: str, status: str) -> AlertResponse | None:
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id, Alert.user_id == user_id)
    )
    alert = result.scalar_one_or_none()
    if alert is None:
        return None
    alert.status = status
    await db.commit()
    await db.refresh(alert)
    return AlertResponse.model_validate(alert)


async def get_stats(db: AsyncSession, user_id: str) -> dict:
    result = await db.execute(select(Alert).where(Alert.user_id == user_id))
    alerts = result.scalars().all()

    total = len(alerts)
    open_count = sum(1 for a in alerts if a.status == "open")
    investigating = sum(1 for a in alerts if a.status == "investigating")
    resolved = sum(1 for a in alerts if a.status == "resolved")
    critical = sum(1 for a in alerts if a.severity == "critical")
    high = sum(1 for a in alerts if a.severity == "high")
    medium = sum(1 for a in alerts if a.severity == "medium")
    low = sum(1 for a in alerts if a.severity == "low")

    return {
        "total_alerts": total,
        "open": open_count,
        "investigating": investigating,
        "resolved": resolved,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
    }
