from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import databases

DATABASE = 'mysql+pymysql'
USER = 'root'
PASSWORD = 'root'
HOST = 'mysql'
#PORT = '3306'
DB_NAME = 'hacku_db'

DATABASE_URL = '{}://{}:{}@{}/{}'.format(DATABASE, USER, PASSWORD, HOST, DB_NAME)

engine = create_engine(
    DATABASE_URL,
    encoding='utf-8',
    echo=True
)

# 実際の DB セッション
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = SessionLocal.query_property()


# Dependency Injection用
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()