from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base_class import Base
from app.models.building import Building


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    activity_id = Column(Integer, ForeignKey("activities.id"))

    building = relationship("Building", back_populates="organizations")
    activity = relationship("Activity", back_populates="organizations")
