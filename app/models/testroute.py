
from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class Items(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255))
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

# ---------- Request Models ----------
class ItemRequestModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the item")
    description: str | None = Field(None, max_length=255, description="Optional item description")

# ---------- Response Models ----------
class ItemResponseModel(BaseModel):
    id: int
    title: str
    description: str | None
    createdAt: datetime

    class Config:
        orm_mode = True 