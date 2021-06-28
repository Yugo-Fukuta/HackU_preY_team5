from database import Base
from sqlalchemy import Column, String, Integer, JSON, UniqueConstraint
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin

class APICacheModel(Base, TimestampMixin):
    __tablename__ = 'api_cache'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    celeb_name = Column(String(100), unique=True, nullable=False)
    yt_cache = Column(JSON, nullable=True)
    tw_cache = Column(JSON, nullable=True)
    nw_cache = Column(JSON, nullable=True)
    wk_cache = Column(JSON, nullable=True)