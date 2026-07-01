import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Well(Base):
    __tablename__ = "wells"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    well_name = Column(String, nullable=False)
    well_type = Column(String, nullable=False)
    status = Column(String, default="active")
    depth = Column(Float, default=0.0)
    pressure = Column(Float, default=0.0)
    temperature = Column(Float, default=0.0)
    flow_rate = Column(Float, default=0.0)
    integrity_score = Column(Integer, default=100)
    last_inspected = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="wells")
    alerts = relationship("Alert", back_populates="well", cascade="all, delete-orphan")
