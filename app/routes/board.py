from fastapi import APIRouter

board_router = APIRouter()


@board_router.get('/list')
def join():
    return {'msg': 'Hello, Board list!'}


@board_router.get('/write')
def login():
    return {'msg': 'Hello, Board write!'}


@board_router.get('/view')
def myinfo():
    return {'msg': 'Hello, Board view!'}

