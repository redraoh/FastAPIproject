import os.path
from datetime import datetime

from app.dbfactory import Session
from sqlalchemy import insert, select, update, func, or_
import requests
from app.models.gallery import Gallery, GalAttach


# 이미지 파일 저장 경로 설정
UPLOAD_DIR = '/opt/homebrew/var/www/cdn'



class GalleryService():
    @staticmethod
    def gallery_convert(gdto):
        # 클라이언트에서 전달받은 데이터를 dict형으로 변환
        data = gdto.model_dump()
        # data.pop('response') # captcha 확인용변수 response는 제거 # 캡챠 사용시 주석처리 제거
        gal = Gallery(**data)   # 보드 클래스와 스키마에 정해져있는거랑 다름. response가 있었는데 여기는 response를 뺴줘야함
        data = {'userid': gal.userid, 'title': gal.title, 'contents': gal.contents}
        return data

    @staticmethod
    def insert_gallery(gdto, fname, fsize):
        # 변환된 회원정보를 member 테이블에 저장
        data = GalleryService.gallery_convert(gdto)
        with Session() as sess:
            stmt = insert(Gallery).values(data)
            result = sess.execute(stmt)
            sess.commit()

            data = {'fname': fname, 'fsize': fsize, 'gno': result.inserted_primary_key[0]}
            print(result.inserted_primary_key)
            stmt = insert(GalAttach).values(data)
            result = sess.execute(stmt)
            sess.commit()
        return result

    @staticmethod
    async def process_upload(attach):
        today = datetime.today().strftime('%Y%m%d%H%M%S')
        nfname = f'{today}{attach.filename}'    # 파일이름
        fsize = attach.size     # 파일크기
        # os.path.join(A, B) => A/B (경로 생성)
        fname = os.path.join(UPLOAD_DIR, nfname)
        # fname = UPLOAD_DIR + '//20240214' + attach.filename # 업로드한 파일이 덮어씌워지는걸 방지. 식별코드,UUID 32비트난수코드 입력.
        # 비동기 처리를 위해 함수에 await 지시자 추가
        # 이럴 경우 함수 정의부분에 async 라는 지시자 추가 필요! await과 async는 항상 따라다닌다
        content = await attach.read()   # 업로드한 파일의 내용을 비동기로(await) 모두 읽어옴, 함수에 async 추가
        with open(fname, 'wb') as f:    # 바이너리 형태로 저장
            f.write(content)            # 파일의 내용을 지정한 파일이름으로 저장

        return nfname, fsize    # 업로드 이후 결과물 리턴

    @staticmethod
    def select_gallery(cpg):
        stnum = (cpg - 1) * 25
        with Session() as sess:
            cnt = sess.query(func.count(Gallery.gno)).scalar()    # 총 게시글 수, scalar 붙여야 값이 넘어옴

            stmt = select(Gallery.gno, Gallery.title, Gallery.userid,
                          Gallery.regdate, Gallery.views, GalAttach.fname)\
                            .join_from(Gallery, GalAttach)\
                            .order_by(Gallery.gno.desc())\
                            .offset(stnum).limit(25)
                            # 조인해서 가져옴
            result = sess.execute(stmt)

        return result, cnt
    #
    # @staticmethod
    # def selectone_board(bno):
    #     with Session() as sess:
    #         stmt = select(Board).filter_by(bno=bno)
    #         result = sess.execute(stmt).first()
    #
    #     return result
    #
    #
    # @staticmethod
    # def update_count_board(bno):
    #     with Session() as sess:
    #         stmt = update(Board).filter_by(bno=bno)\
    #             .values(views=Board.views+1)
    #         result = sess.execute(stmt)
    #         sess.commit()
    #
    #     return result
    #
    #
    # @staticmethod
    # def find_select_board(ftype, fkey, cpg):
    #     stnum = (cpg - 1) * 25
    #     stnum = 0
    #     with Session() as sess:
    #
    #         stmt = select(Board.bno, Board.title, Board.userid,
    #                       Board.regdate, Board.views)
    #
    #         # 동적쿼리(다이나믹쿼리) 작성 - 조건에 따라 where절이 바뀜
    #         myfilter = Board.title.like(fkey)
    #         if ftype == 'userid': myfilter = Board.userid.like(fkey)
    #         elif ftype == 'contents': myfilter = Board.contents.like(fkey)
    #         elif ftype == 'titconts': myfilter = or_(Board.title.like(fkey), Board.contents.like(fkey)) # and_, not_ 등등 사용가능
    #         elif ftype == 'comments': myfilter = Board.comments.like(fkey)
    #
    #         stmt = stmt.filter(myfilter).order_by(Board.bno.desc()).offset(stnum).limit(25)
    #         result = sess.execute(stmt)
    #
    #         cnt = sess.query(func.count(Board.bno))\
    #             .filter(myfilter).scalar()    # 검색한 이후 게시글 수, scalar 붙여야 값이 넘어옴
    #
    #     return result, cnt
    #
    #
    #
    # # google recaptcha 확인 url
    # # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    # @staticmethod
    # def check_captcha(gdto):
    #     data = gdto.model_dump()    # 클라이언트가 보낸 객체를 dict로 변경
    #     req_url = 'https://www.google.com/recaptcha/api/siteverify'
    #     params = { 'secret': '구글 시크릿 키 입력',
    #                'response': data['response'] }
    #     res = requests.get(req_url, params=params)
    #     result = res.json()
    #     # print('check', result)
    #
    #     # return result['success']
    #     return True