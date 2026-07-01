from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services.auth import register, login

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register_endpoint(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register(db, data)


@router.post("/login", response_model=TokenResponse)
async def login_endpoint(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login(db, data)
