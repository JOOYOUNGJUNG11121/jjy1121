from werkzeug.security import generate_password_hash
from app.models import User, Store, Employee
from . import db
import random


def create_user(data):
    # 데이터 검증
    if not data:
        return {"error": "No input data provided"}, 400

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
        return {"error": "Email already exists"}, 400

    # 비밀번호 해싱 및 사용자 생성
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

    return {"message": "User created successfully", "user_id": new_user.id}, 201

def create_store(data):
    # 데이터 검증
    if not data:
        return {"error": "No input data provided"}, 400

    # 데이터 추출
    name = data.get('name')
    address = data.get('address')
    contact = data.get('contact')

    # 가게 생성
    new_store = Store(
        name=name,
        address=address,
        contact=contact
    )
    db.session.add(new_store)
    db.session.commit()

    return {"message": "Store created successfully", "store_id": new_store.id}, 201

def register_employee(data):
    # 데이터 검증
    if not data:
        return {"error": "No input data provided"}, 400

    # 데이터 추출
    user_id = data.get('user_id')
    store_id = data.get('store_id')
    employee_type = data.get('type')

    # 유효성 검사
    user = User.query.get(user_id)
    store = Store.query.get(store_id)

    if not user or not store:
        return {"error": "User or Store not found"}, 404

    employee_code = str(random.randint(100000, 999999))
    # 직원 등록
    new_employee = Employee(
        code=employee_code,
        user_id=user_id,
        store_id=store_id,
        type=employee_type
    )
    db.session.add(new_employee)
    db.session.commit()

    return {"message": "Employee registered successfully", "employee_id": new_employee.id}, 201
