from flask import Blueprint, request, jsonify
from app.services import create_user, create_store, register_employee

# Employee, Store, User 관련 API를 담당할 Blueprint 정의
route_bp = Blueprint('route', __name__, url_prefix='/api')

# Employee 등록
@route_bp.route('/employees', methods=['POST'])
def register_employee_route():
    data = request.json
    response, status = register_employee(data)
    return jsonify(response), status

# Store 생성
@route_bp.route('/stores', methods=['POST'])
def create_store_route():
    data = request.json
    response, status = create_store(data)
    return jsonify(response), status

# User 가입
@route_bp.route('/signup', methods=['POST'])
def signup_user():
    data = request.json
    response, status = create_user(data)
    return jsonify(response), status
