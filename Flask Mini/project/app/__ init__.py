from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from . import config


# SQLAlchemy 및 Flask-Migrate 초기화
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Flask 애플리케이션 생성
    app = Flask(__name__)

    # 애플리케이션 설정 로드
    app.config.from_object(config.Config)

    # 데이터베이스 및 마이그레이션 초기화
    db.init_app(app)
    migrate.init_app(app, db)

    return app

from flask import Flask, request, jsonify
from app.services import create_user, create_store, register_employee

# SQLAlchemy 및 Flask-Migrate 초기화
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    # 인덱스 페이지 (API 안내)
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to My API!',
            'endpoints': {
                '/api/users/signup': 'User Signup',
                '/api/stores': 'Create Store',
                '/api/employees': 'Register Employee'
            }
        })

    # User 회원가입 (서비스 호출)
    @app.route('/api/users/signup', methods=['POST'])
    def signup_user():
        data = request.json
        try:
            new_user = create_user(data)
            return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Store 생성 (서비스 호출)
    @app.route('/api/stores', methods=['POST'])
    def create_store_route():
        data = request.json
        try:
            new_store = create_store(data)
            return jsonify({"message": "Store created successfully", "store_id": new_store.id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Employee 등록 (서비스 호출)
    @app.route('/api/employees', methods=['POST'])
    def register_employee_route():
        data = request.json
        try:
            new_employee = register_employee(data)
            return jsonify({
                "message": "Employee registered successfully", 
                "employee_id": new_employee.id, 
                "employee_code": new_employee.code
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from config import Config

# SQLAlchemy 및 Flask-Migrate 초기화
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Flask 애플리케이션 생성
    app = Flask(__name__)

    # 애플리케이션 설정 로드
    app.config.from_object(Config)

    # 데이터베이스 및 마이그레이션 초기화
    db.init_app(app)
    migrate.init_app(app, db)

		# 인덱스 페이지 (API 안내)
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to My API!',
            'endpoints': {
                '/api/users/signup': 'User Signup',
                '/api/stores': 'Create Store',
                '/api/employees': 'Register Employee'
            }
        })

    # User 회원가입
    @app.route('/api/users/signup', methods=['POST'])
    def signup_user():
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            # 데이터 추출
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            address = data.get('address')
            contact = data.get('contact')
            gender = data.get('gender')

            # 유효성 검사
            if User.query.filter_by(email=email).first():
                return jsonify({"error": "Email already exists"}), 400

            # 비밀번호 해싱 및 저장
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password,
                address=address,
                contact=contact,
                gender=gender
            )
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "User created successfully", "user_id": new_user.id}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Store 생성
    @app.route('/api/stores', methods=['POST'])
    def create_store():
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            # 데이터 추출
            name = data.get('name')
            address = data.get('address')
            contact = data.get('contact')

            new_store = Store(
                name=name,
                address=address,
                contact=contact
            )
            db.session.add(new_store)
            db.session.commit()

            return jsonify({"message": "Store created successfully", "store_id": new_store.id}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Employee 등록
    @app.route('/api/employees', methods=['POST'])
    def register_employee():
        data = request.json
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        try:
            # 데이터 추출
            user_id = data.get('user_id')
            store_id = data.get('store_id')
            employee_type = data.get('type')

            # 유효성 검사
            user = User.query.get(user_id)
            store = Store.query.get(store_id)

            if not user or not store:
                return jsonify({"error": "User or Store not found"}), 404

            # 직원번호 (랜덤 번호 생성)
            from random import randint
            employee_code = randint(1000, 9999)

            # 새로운 직원 등록
            new_employee = Employee(
                user_id=user_id,
                store_id=store_id,
                type=employee_type,
                code=employee_code  # 직원번호 삽입
            )
            db.session.add(new_employee)
            db.session.commit()

            return jsonify({"message": "Employee registered successfully", "employee_id": new_employee.id, "employee_code": new_employee.code}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

# project/__init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from . import config

# db와 migrate 객체 선언
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    # 데이터베이스 초기화
    db.init_app(app)
    migrate.init_app(app, db)

    # 인덱스 페이지 (API 안내)
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to My API!',
            'endpoints': {
                '/users/signup': 'User Signup',
                '/stores': 'Create Store',
                '/employees': 'Register Employee'
            }
        })

    # route_bp 가져오기 (블루프린트 등록)
    from .routes import route_bp

    # 블루프린트 등록
    app.register_blueprint(route_bp)

    return app