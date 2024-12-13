from flask import Blueprint, render_template, url_for, jsonify, request
from werkzeug.utils import redirect

# models.py에서 Question 클래스를 가져와서 사용
from pybo import db
from pybo.models import Question
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from pybo.models import User

# 객체 bp 생성
bp = Blueprint('main', __name__, url_prefix='/')
# url_prefix = '/'
# 밑에 접속하는 주소의 기본값
# 예) url_prefix = '/main'
# localhost:5000/main

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


# @bp.route('/')
# def index():
        # 밑에 코드가 db question 테이블 정보를 가져옴
#     question_list = Question.query.order_by(Question.create_date.desc())
        # render_template("html 파일 경로", html의 변수 = python 변수)
        # db에서 query해서 가져 온 question_list를 question_list.html 안의 question_list에 대입
#     return render_template('question/question_list.html', question_list=question_list)
    #return 'Pybo index'


@bp.route('/')
def index():
    return redirect(url_for('question._list'))

@bp.route('/detail/<int:question_id>/')
def detail(question_id): 
    # DB에서 question_Id로 question 자료를 가져옴
    question = Question.query.get_or_404(question_id)   
    # render_template : DB에서 가져온 question을 템플릿에 입력
    return render_template('question/question_detail.html', question=question)

@bp.route('/test')
def test():
    # 관련 웹페이지 주소 리턴
    # 1. redirect('페이지 url')
    # 2. render_template() 페이지를 template 사용하는 경우 이용
    # 3. redirect(url_for('다른 라우트에 있는 페이지'))
    return render_template('test.html')

@bp.route('/test2')
def test2():
    return render_template('test/test2.html')

# get 방식(get 방식일 경우 methods 생략 가능)
@bp.route('/load_question')
def load_question():
    # 1. DB에서 값 읽어오기
    # Questino.query.~~~~
    # [클래스]  쿼리   쿼리 종류
    # Question.query.all() # 모든 레코드 조회
    # Question.query.first() # 첫 번째 레코드 조회
    # Question.query.get(id) # 특정 id로 조회
    # Question.query.filter_by(field=value) # 단순 조건 필터링
    # Question.query.filter_by(Question.field == value) # 보다 복잡한 조건 필터링
    # Question.query.order_by(Question.create_date.desc()) create_date 컬럼을 기준으로 역순으로 정렬
    
    question_list = Question.query.all()
    # question_list = Question.query.order_by(Question.create_date.desc())
    print("question 리스트 : ", question_list)
    # 2. JSON 변환
    question_list_dict = [question.to_dict() for question in question_list]
    # 3. 변환 결과를 return
    return jsonify(question_list_dict)
    # return render_template('question/question_list.html', question_list=question_list)

# methods가 생략되어 있지만 GET 방식으로 query 가져올 수 있음
# http://<주소>/load_question_id?id=<번호>
@bp.route('/load_question_id', methods=['GET'])
def load_question_id():
    # 1. 요청 데이터 가져오기
    # request는 맨 위에 from flask import request 해줘야 함
    id = request.args.get('id')
    
    # 2. 기본 조회 : 모든 데이터
    if not id:
        return "id 값이 없습니다."
    else:
        # id 값을 기준으로 필터링
        question = Question.query.get(id)

    return jsonify(question.to_dict())


# 엔드포인트(주소)는 같아도 방식이 다르면 다르게 인식
# 문제는 없음. 단, 많이 엔드페인트가 겹치다보면 헷갈릴 수가 있음
@bp.route('/load_question_id', methods=['POST'])
# POST 방식은 JSON으로 데이터를 가져옴
# GET 방식과는 다르게 id 값을 가져와야 함
def load_question_id_post():
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "id" 필드를 가져옴
    data = request.get_json()
    print("data : ", data)
    id = data.get('id') if data else None
    
    # 2. 기본 조회 : 모든 데이터
    if not id:
        return jsonify({"error" : "id 값이 없습니다."}), 400
    
    # 3. 데이터 조회
    question = Question.query.get(id)
    if not question:
        return jsonify({"error" : "id {id}에 해당되는 데이터가 없습니다."}), 404

    return jsonify(question.to_dict())

# 엔드포인트(주소)는 같아도 방식이 다르면 다르게 인식
# 문제는 없음. 단, 많이 엔드페인트가 겹치다보면 헷갈릴 수가 있음
@bp.route('/add_question', methods=['POST'])
# POST 방식은 JSON으로 데이터를 가져옴
# GET 방식과는 다르게 id 값을 가져와야 함
def add_question_post():
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "content, subject" 필드를 가져옴
    data = request.get_json()
    print("data : ", data)
    subject = data.get('subject') if data else None
    content = data.get('content') if data else None

    # 3. 새로운 Question 객체 생성
    new_question = Question(
        subject = subject,
        content = content,
        create_date = datetime.now()
    )

    # 데이터베이스 세션에 추가
    db.session.add(new_question)

    # db.session.commit() 것이 데이터를 추가한 것을 커밋
    # db.session.commit() 문제가 발생하면?
    # 문제가 발생하면 서버 프로그램이 중단
    # try, except 구문을 사용하면 문제 발생이 되었을 때
    # 적절한 코드가 실행이 되면서 종료되지 않음
    # try, except 구문을 사용하여 처리해야 함

    try:    
        # 변경사항 커밋
        db.session.commit()
        print("Commit Successful!")
    except SQLAlchemyError as e:
        # SQLAlchemyError를 상요하기 위해서
        # 상단에 from sqlalchemy.exc import SQLAlchemyError 추가
        db.session.rollback()
        print(f"Commit Failed: {str(e)}")
        return jsonify({"error":"데이터 추가 실패 " + str(e)}), 500
    # 4. 결과 반환
    return jsonify({"message":"추가가 완료되었습니다."}), 201

# PUT 방식 구현
# http://<주소IP>/change_question/<int:id>
# request의 본문
# {
#   "subject" : "주제",
#   "content" : "내용"
# }
# id와 subject, content를 가져오는 방식이 약간 다름
@bp.route('/change_question/<int:id>', methods=['PUT'])
def change_question(id):
    # 1. 요청 데이터 가져오기
    data = request.get_json()
    print("data : ", data)
    subject = data.get('subject') if data else None
    content = data.get('content') if data else None

    # id로 DB에 Question 테이블을 조회해서 데이터를 업데이트하는 것이 목적

    # 2. id로 DB Question 테이블의 데이터를 조회
    question = Question.query.get(id)
    
    # question이 없다면
    if not question:
        return jsonify({"error",f"id {id}에 해당하는 데이터가 없습니다."}), 404
    
    # 데이터가 존재하면 데이터 업데이트
    if subject:
        question.subject = subject

    if content:
        question.content = content 

    # 데이터베이스 세션에 추가
    db.session.add(question)

    # db.session.commit() 것이 데이터를 추가한 것을 커밋
    # db.session.commit() 문제가 발생하면?
    # 문제가 발생하면 서버 프로그램이 중단
    # try, except 구문을 사용하면 문제 발생이 되었을 때
    # 적절한 코드가 실행이 되면서 종료되지 않음
    # try, except 구문을 사용하여 처리해야 함

    try:    
        # 변경사항 커밋
        db.session.commit()
        print("Update Successful!")
    except SQLAlchemyError as e:
        # SQLAlchemyError를 상요하기 위해서
        # 상단에 from sqlalchemy.exc import SQLAlchemyError 추가
        db.session.rollback()
        print(f"Update Failed: {str(e)}")
        return jsonify({"error":"업데이트 중 문제가 발생하였습니다." + str(e)}), 500
    # 4. 결과 반환
    return jsonify({"message":f"Question {id}이 업데이트 되었습니다."}), 201

# DELETE 방식 구현
# http://<주소IP>/delete_question/<int:id>
@bp.route('/delete_question/<int:id>', methods=['DELETE'])
def delete_question(id):
    # id로 DB에 Question 테이블을 조회해서 데이터를 삭제하는 것이 목적

    # 1. id로 DB Question 테이블의 데이터를 조회
    question = Question.query.get(id)
    
    # question이 없다면
    if not question:
        return jsonify({"error",f"id {id}에 해당하는 데이터가 없습니다."}), 404
    
    # 2. 데이터 삭제
    try:
        db.session.delete(question)
        db.session.commit()
        print(f"Question {id} has benn deleted.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Delete Failed: {str(e)}")
        return jsonify({"error":"삭제 중 문제가 발생하였습니다." + str(e)}), 500 
    
    # 3. 결과 반환
    return jsonify({"message":f"Question {id}이 삭제 되었습니다."}), 201

# 엔드포인트(주소)는 같아도 방식이 다르면 다르게 인식
# 문제는 없음. 단, 많이 엔드페인트가 겹치다보면 헷갈릴 수가 있음
@bp.route('/add_user', methods=['POST'])
def add_user():
    # 1. 요청 데이터 가져오기
    # JSON 요청에서 "content, subject" 필드를 가져옴
    data = request.get_json()
    user_id = data.get('user_id') if data else None
    password = data.get('password') if data else None

    if not user_id or not password:
        return jsonify({"error":"user_id와 password는 필수 항목입니다."}), 400
    
    # 3. 새로운 User 객체 생성
    new_user = User(
        user_id = user_id,
        password = password
    )

    try:   
        # 데이터베이스 세션에 추가
        db.session.add(new_user) 
        # 변경사항 커밋
        db.session.commit()
        print(f"User {user_id}가 추가 되었습니다.")
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Commit Failed: {str(e)}")
        return jsonify({"error":"사용자 추가 중 문제가 발생하였습니다. " + str(e)}), 500
    # 4. 결과 반환
    return jsonify({"message":f"User {user_id}가 추가되었습니다."}), 201