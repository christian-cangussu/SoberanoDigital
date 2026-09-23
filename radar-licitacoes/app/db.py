from datetime import datetime
from sqlalchemy import create_engine, String, Text, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Opportunity(Base):
    __tablename__ = "opportunities"
    __table_args__ = (UniqueConstraint("external_id", name="uq_opportunity_external_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str] = mapped_column(String(500))
    title: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(Text, default="")
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    score: Mapped[int] = mapped_column(Integer, default=0)
    matched_keywords: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
