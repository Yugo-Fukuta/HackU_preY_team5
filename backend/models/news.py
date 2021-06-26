from database import Base
from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin

class NewsModel(Base, TimestampMixin):
    __tablename__ = 'news'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    whose = Column(String(20), nullable=False)
    nankome = Column(Integer, nullable=False)
    api_key = Column(String(50), unique=True, nullable=False)
    __table_args__ = (UniqueConstraint(
        'whose', 'nankome', name='unique_whose_nankome'),) 