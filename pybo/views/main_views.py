from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

# models.py에서 Question 클래스를 가져와서 사용
from pybo.models import Question

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
