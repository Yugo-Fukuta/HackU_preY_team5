from database import Base
from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin

class OshidoModel(Base, TimestampMixin):
    __tablename__ = 'oshido'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(String(50), nullable=False)
    celeb_name = Column(String(100), nullable=False)
    oshido = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint(
        'uid', 'celeb_name', name='unique_uid_celeb_name'),)  # uidとceleb_nameの組み合わせで一意になる