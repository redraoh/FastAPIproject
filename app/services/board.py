from app.models.board import Board
from app.dbfactory import Session
from sqlalchemy import insert, select, update, func

class BoardService():
    @staticmethod
    def board_convert(bdto):
        # 클라이언트에서 전달받은 데이터를 dict형으로 변환
        data = bdto.model_dump()
        bd = Board(**data)
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
    def find_select_board(ftype, fkey):
        # stnum = (cpg - 1) * 25
        stnum = 0
        with Session() as sess:
            cnt = sess.query(func.count(Board.bno)).scalar()    # 총 게시글 수, scalar 붙여야 값이 넘어옴

            stmt = select(Board.bno, Board.title, Board.userid,
                          Board.regdate, Board.views)

            # 동적쿼리(다이나믹쿼리) 작성 - 조건에 따라 where절이 바뀜
            myfilter = Board.title.like(fkey)
            if ftype == 'userid': myfilter = Board.userid.like(fkey)
            elif ftype == 'contents': myfilter = Board.contents.like(fkey)

            stmt = stmt.filter(myfilter).order_by(Board.bno.desc()).offset(stnum).limit(25)
            result = sess.execute(stmt)

        return result