from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

# from sqlalchemy.orm import DeclarativeBase


# class Base(DeclarativeBase):
#     pass
Base = declarative_base()

class Board(Base):
    __tablename__ = 'board'

    bno = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(18), nullable=False)
    userid = Column(String(18), nullable=False)
    regdate = Column(DateTime, default=datetime.now)
    views = Column(Integer, default=0)
    contents = Column(Text, nullable=False)


# 테이블의 구조를 나타냄, 자동으로 테이블 만들어주는 ORM 기능 = models/board.py
