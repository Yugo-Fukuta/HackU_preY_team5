from database import Base
from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin

class TrendModel(Base, TimestampMixin):
    __tablename__ = 'trend'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    celeb_name = Column(String(100), unique=True, nullable=False)
    count = Column(Integer, nullable=False)