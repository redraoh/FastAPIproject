from datetime import datetime

from pydantic import BaseModel


class Board(BaseModel):
    bno: int
    title: str
    userid: str
    regdate: datetime
    views: int
    contents: str

    class Config:
        from_attributes = True


class NewBoard(BaseModel):
    title: str
    userid: str
    contents: str

# 정해진규칙에 데이터를 보내는지확인이 가능. models/board 에사용한 컬럼 이름이 동일해야함.