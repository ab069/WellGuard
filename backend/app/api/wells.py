from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.well import WellCreate, WellResponse
from app.services.well_service import create_well, list_wells, get_well, get_stats

router = APIRouter(prefix="/api/wells", tags=["wells"])


@router.post("", response_model=WellResponse, status_code=status.HTTP_201_CREATED)
async def create_well_endpoint(
    data: WellCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await create_well(db, user_id, data)


@router.get("", response_model=list[WellResponse])
async def list_wells_endpoint(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await list_wells(db, user_id)


@router.get("/stats")
async def wells_stats(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await get_stats(db, user_id)


@router.get("/{well_id}", response_model=WellResponse)
async def get_well_endpoint(
    well_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await get_well(db, well_id, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Well not found")
    return result
