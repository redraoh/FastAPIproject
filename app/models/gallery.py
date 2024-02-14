from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column

# from sqlalchemy.orm import DeclarativeBase


# class Base(DeclarativeBase):
#     pass
Base = declarative_base()

class Gallery(Base):
    __tablename__ = 'gallery'

    gno = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(18), nullable=False)
    userid = Column(String(18), nullable=False)
    regdate = Column(DateTime, default=datetime.now)
    views = Column(Integer, default=0)
    contents = Column(Text, nullable=False)
    # ga = relationship

class GalAttach(Base):
    __tablename__ = 'galattach'

    gano = Column(Integer, primary_key=True, autoincrement=True)
    gno = mapped_column(Integer, ForeignKey('gallery.gno'))  # 외부키 가져오기
    fname = Column(String(50), nullable=False)
    fszie = Column(Integer, default=0)
