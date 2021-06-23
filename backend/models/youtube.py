from database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin

class YouTubeModel(Base, TimestampMixin):
    __tablename__ = 'youtube'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    whose = Column(String(20), nullable=False)
    nankome = Column(Integer, nullable=False)
    api_key = Column(String(50), nullable=False)