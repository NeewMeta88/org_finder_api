from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.models.base_class import Base


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    organizations = relationship("Organization", back_populates="building")
