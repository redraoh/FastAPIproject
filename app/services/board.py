from app.models.board import Board
from app.dbfactory import Session
from sqlalchemy import insert, select, update

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
    def select_board():
        with Session() as sess:
            stmt = select(Board.bno, Board.title, Board.userid,
                          Board.regdate, Board.views)\
                            .order_by(Board.bno.desc())\
                            .offset(0).limit(25)
            result = sess.execute(stmt)

        return result

    @staticmethod
    def selectone_board(bno):
        with Session() as sess:
            stmt = select(Board).filter_by(bno=bno)
            result = sess.execute(stmt).first()

        return result


    @staticmethod
    def update_count_board(bno):
        with Session() as sess:
            stmt = update(Board).filter_by(bno=bno).values(views=Board.views+1)
            result = sess.execute(stmt)
            sess.commit()

        return result


