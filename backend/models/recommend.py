from database import Base
from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin

class RecommendModel(Base, TimestampMixin):
    __tablename__ = 'recommend'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(String(50), unique=True, nullable=False)
    recommend = Column(String(100), nullable=True)