from flask import Flask
# app 객체를 전체 전역으로 사용
# 프로젝트 규모가 커질수록 문제가 발생
# 문제 : 순환 참조 오류
# app = Flask(__name__)

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

# 애플리케이션 팩토리 완성
# create_app() 함수 안에
# app 이라는 Flask 인스턴스를 생성해서 작동하게 함
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    
    # '/' 주소가 호출이 되면
    # 밑에 있는 hello_pybo가 실행됨
    # @app.route와 같은 애너테이션으로 url을 매핑하는 함수를 라우팅 함수
    # @app.route('/')
    # hello_pybo() 는 라우팅 함수
    #def hello_pybo():
        #return 'Hello, Pybo!'

    # 만약 새로운 url 매핑이 필요하면 라우팅 함수를 create_app 함수 안에 계속 추가해야 한다.
    # 그러면 create_app 함수는 엄청나게 크고 복잡한 함수가 된다.
    # ORM -> DB와 연관이 됨
    db.init_app(app)
    migrate.init_app(app, db)
    # models.py 파일을 import해서 사용( . 인 이유는 현재 __init__.py 와 models.py가 같은 경로상에 존재하므로)
    from . import models

    # 블루프린트
    # -> 블루프린트(Blueprint)를 사용해서 관리
    # views 폴더 안에 main_views라는 py파일을 import해서 사용
    from .views import main_views
    # main_views.py에 생성된 bp 객체를 등록
    app.register_blueprint(main_views.bp)


    return app