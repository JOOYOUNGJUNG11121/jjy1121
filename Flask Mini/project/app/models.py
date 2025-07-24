from . import db
from enum import Enum


# 직급을 위한 Enum 정의
class EmployeeTypeEnum(Enum):
    STAFF = "STAFF"
    MANAGER = "MANAGER"


# 성별을 위한 Enum 정의
class GenderEnum(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(50))
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    employees = db.relationship('Employee', back_populates='user')


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255))
    contact = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    employees = db.relationship('Employee', back_populates='store')


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)  # Employee code
    type = db.Column(db.Enum(EmployeeTypeEnum), nullable=False)  # Python Enum 사용
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Foreign key references
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='employees')
    store = db.relationship('Store', back_populates='employees')
