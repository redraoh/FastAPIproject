from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import status

from app.schemas.board import NewBoard
from app.services.board import BoardService

from math import ceil


board_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')
board_router.mount('/static', StaticFiles(directory='views/static'), name='static')

# 페이징 알고리즘
# 페이지당 게시글 수 : 25개 지정
# 1 page : 1 ~ 25
# 2 page : 26 ~ 50
# 3 page : 51 ~ 75
# ...
# n page : (n-1)*25+1 ~ 25*n

# 페이지네이션 알고리즘
# 현재페이지에 따라 보여줄 페이지 블록 결정
# ex) 총 페이지수 : 27일
# cpg = 1: 1 2 3 4 5 6 7 8 9 10
# cpg = 3: 1 2 3 4 5 6 7 8 9 10
# cpg = 9: 1 2 3 4 5 6 7 8 9 10
# cpg = 11: 11 12 13 14 15 16 17 18 19 20
# cpg = 17: 11 12 13 14 15 16 17 18 19 20
# cpg = 23: 21 22 23 24 25 26 27
# cpg = n: m m+1 m+2 ... m+9
# 따라서, cpg에 따라 페이지블록의 시작값 계산
# m = ((cpg - 1) / 10) * 10 + 1 // cpg는 정수가 되어야함.


@board_router.get('/list/{cpg}', response_class=HTMLResponse)
def list(req: Request, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1     # 페이지네이션 시작값
    bdlist, cnt = BoardService.select_board(cpg)
    allpage = ceil( cnt / 25 )  # 총페이지수(올림해줌)
    return templates.TemplateResponse('/board/list.html',{'request': req, 'bdlist': bdlist,
                                                          'cpg': cpg, 'stpg': stpg, 'allpage': allpage})

    # request 객체로 보냄
@board_router.get('/write', response_class=HTMLResponse)
def write(req: Request):
    return templates.TemplateResponse('/board/write.html',{'request': req})

@board_router.post('/write')
def writeok(bdto: NewBoard):
    result = BoardService.insert_board(bdto)
    res_url = '/error'
    if result.rowcount > 0: res_url = '/board/list'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)

@board_router.get('/view/{bno}', response_class=HTMLResponse)
def view(req: Request, bno:str):
    bd = BoardService.selectone_board(bno)[0]
    BoardService.update_count_board(bno)
    return templates.TemplateResponse('/board/view.html',{'request': req, 'bd': bd})


# 검색
@board_router.get('/list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
def find(req: Request, ftype: str, fkey: str):
    # stpg = int((cpg - 1) / 10) * 10 + 1     # 페이지네이션 시작값
    bdlist = BoardService.find_select_board(ftype, '%'+fkey+'%')
    # allpage = ceil( cnt / 25 )  # 총페이지수(올림해줌)
    return templates.TemplateResponse('/board/list.html',{'request': req, 'bdlist': bdlist,'cpg': 1, 'stpg': 1, 'allpage': 10})