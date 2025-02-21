from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from domain.BaseModel import Base


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    min_volume: Mapped[int] = mapped_column(Integer)
    max_volume: Mapped[int] = mapped_column(Integer)
    tick_size: Mapped[float] = mapped_column(Float)