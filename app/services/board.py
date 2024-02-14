from app.models.board import Board
from app.dbfactory import Session
from sqlalchemy import insert, select, update, func, or_
import requests


class BoardService():
    @staticmethod
    def board_convert(bdto):
        # 클라이언트에서 전달받은 데이터를 dict형으로 변환
        data = bdto.model_dump()
        data.pop('response') # captcha 확인용변수 response는 제거
        bd = Board(**data)   # 보드 클래스와 스키마에 정해져있는거랑 다름. response가 있었는데 여기는 response를 뺴줘야함
        data = {'userid': bd.userid, 'title': bd.title, 'contents': bd.contents}
        return data

    @staticmethod
    def insert_board(bdto):
        # 변환된 회원정보를 member 테이블에 저장
        data = BoardService.board_convert(bdto)
        with Session() as sess:
            stmt = insert(Board).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result

    @staticmethod
    def select_board(cpg):
        stnum = (cpg - 1) * 25
        with Session() as sess:
            cnt = sess.query(func.count(Board.bno)).scalar()    # 총 게시글 수, scalar 붙여야 값이 넘어옴

            stmt = select(Board.bno, Board.title, Board.userid,
                          Board.regdate, Board.views)\
                            .order_by(Board.bno.desc())\
                            .offset(stnum).limit(25)
            result = sess.execute(stmt)

        return result, cnt

    @staticmethod
    def selectone_board(bno):
        with Session() as sess:
            stmt = select(Board).filter_by(bno=bno)
            result = sess.execute(stmt).first()

        return result


    @staticmethod
    def update_count_board(bno):
        with Session() as sess:
            stmt = update(Board).filter_by(bno=bno)\
                .values(views=Board.views+1)
            result = sess.execute(stmt)
            sess.commit()

        return result


    @staticmethod
    def find_select_board(ftype, fkey, cpg):
        stnum = (cpg - 1) * 25
        stnum = 0
        with Session() as sess:

            stmt = select(Board.bno, Board.title, Board.userid,
                          Board.regdate, Board.views)

            # 동적쿼리(다이나믹쿼리) 작성 - 조건에 따라 where절이 바뀜
            myfilter = Board.title.like(fkey)
            if ftype == 'userid': myfilter = Board.userid.like(fkey)
            elif ftype == 'contents': myfilter = Board.contents.like(fkey)
            elif ftype == 'titconts': myfilter = or_(Board.title.like(fkey), Board.contents.like(fkey)) # and_, not_ 등등 사용가능
            elif ftype == 'comments': myfilter = Board.comments.like(fkey)

            stmt = stmt.filter(myfilter).order_by(Board.bno.desc()).offset(stnum).limit(25)
            result = sess.execute(stmt)

            cnt = sess.query(func.count(Board.bno))\
                .filter(myfilter).scalar()    # 검색한 이후 게시글 수, scalar 붙여야 값이 넘어옴

        return result, cnt

    # google recaptcha 확인 url
    # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    @staticmethod
    def check_captcha(bdto):
        data = bdto.model_dump()    # 클라이언트가 보낸 객체를 dict로 변경
        req_url = 'https://www.google.com/recaptcha/api/siteverify'
        params = { 'secret': '구글 시크릿 키 입력',
                   'response': data['response'] }
        res = requests.get(req_url, params=params)
        result = res.json()
        # print('check', result)

        # return result['success']
        return True