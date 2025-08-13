from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from ..extensions import db, bcrypt
from ..models import User, Role
from ..schemas import RegisterSchema, LoginSchema
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()

@auth_bp.post("/register")
@swag_from({
  "tags": ["Auth"],
  "summary": "Register a new user",
  "requestBody": {"required": True, "content": {"application/json": {"schema": RegisterSchema}}}
})
def register():
    payload = request.get_json() or {}
    data = register_schema.load(payload)
    if User.query.filter_by(email=data["email"]).first():
        return {"message": "Email already registered"}, 409
    user = User(email=data["email"], password_hash=bcrypt.generate_password_hash(data["password"]).decode())
    # Give first user admin role (simple bootstrap)
    if User.query.count() == 0:
        admin = Role.query.filter_by(name="admin").first() or Role(name="admin")
        db.session.add(admin)
        user.roles.append(admin)
    db.session.add(user)
    db.session.commit()
    return {"message": "Registered"}, 201

@auth_bp.post("/login")
@swag_from({
  "tags": ["Auth"],
  "summary": "Login and get JWT token",
  "requestBody": {"required": True, "content": {"application/json": {"schema": LoginSchema}}}
})
def login():
    payload = request.get_json() or {}
    data = login_schema.load(payload)
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data["password"]):
        return {"message": "Invalid credentials"}, 401
    token = create_access_token(identity={"id": user.id, "email": user.email, "roles": [r.name for r in user.roles]})
    return {"access_token": token}, 200
