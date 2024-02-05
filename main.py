from fastapi import FastAPI

from app.routes.board import board_router
from app.routes.member import member_router

app = FastAPI()

# 외부 route 파일 불러오기
app.include_router(member_router)
app.include_router(board_router, prefix='/board')   # 경로를 줄여줌


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '_main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
