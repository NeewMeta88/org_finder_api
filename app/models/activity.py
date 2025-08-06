from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_class import Base


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship(lambda: Activity, remote_side=[id], back_populates="children")
    children = relationship(lambda: Activity, back_populates="parent", cascade="all, delete-orphan")
    organizations = relationship("Organization", back_populates="activity")