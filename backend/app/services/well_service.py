from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.well import Well
from app.schemas.well import WellCreate, WellResponse


async def create_well(db: AsyncSession, user_id: str, data: WellCreate) -> WellResponse:
    well = Well(user_id=user_id, **data.model_dump())
    db.add(well)
    await db.commit()
    await db.refresh(well)
    return WellResponse.model_validate(well)


async def list_wells(db: AsyncSession, user_id: str) -> list[WellResponse]:
    result = await db.execute(
        select(Well).where(Well.user_id == user_id).order_by(Well.created_at.desc())
    )
    return [WellResponse.model_validate(w) for w in result.scalars().all()]


async def get_well(db: AsyncSession, well_id: str, user_id: str) -> WellResponse | None:
    result = await db.execute(
        select(Well).where(Well.id == well_id, Well.user_id == user_id)
    )
    well = result.scalar_one_or_none()
    if well is None:
        return None
    return WellResponse.model_validate(well)


async def get_stats(db: AsyncSession, user_id: str) -> dict:
    result = await db.execute(select(Well).where(Well.user_id == user_id))
    wells = result.scalars().all()

    total = len(wells)
    active = sum(1 for w in wells if w.status == "active")
    avg_integrity = round(sum(w.integrity_score for w in wells) / total, 1) if total > 0 else 0

    from app.models.alert import Alert
    alert_result = await db.execute(
        select(func.count(Alert.id)).where(
            Alert.user_id == user_id,
            Alert.severity.in_(["critical", "high"]),
            Alert.status != "resolved",
        )
    )
    critical_alerts = alert_result.scalar() or 0

    return {
        "total_wells": total,
        "active_wells": active,
        "critical_alerts": critical_alerts,
        "avg_integrity_score": avg_integrity,
    }
