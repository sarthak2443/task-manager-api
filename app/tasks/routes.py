from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import or_
from ..extensions import db
from ..models import Task, User
from ..schemas import TaskCreateSchema, TaskUpdateSchema, TaskOutSchema
from flasgger import swag_from

tasks_bp = Blueprint("tasks", __name__)
create_schema = TaskCreateSchema()
update_schema = TaskUpdateSchema()
out_schema = TaskOutSchema()
out_list_schema = TaskOutSchema(many=True)

def current_user():
    payload = get_jwt()
    return User.query.get(payload["sub"]["id"]) if payload and "sub" in payload else None

def is_admin():
    payload = get_jwt()
    roles = payload.get("sub", {}).get("roles", [])
    return "admin" in roles

@tasks_bp.get("/")
@jwt_required()
@swag_from({
  "tags": ["Tasks"],
  "summary": "List tasks (paginated)",
  "parameters": [
    {"in": "query", "name": "page", "schema": {"type": "integer", "default": 1}},
    {"in": "query", "name": "per_page", "schema": {"type": "integer", "default": 10}},
    {"in": "query", "name": "completed", "schema": {"type": "boolean"}},
    {"in": "query", "name": "all", "schema": {"type": "boolean", "default": False},
     "description": "Admin only: list all users' tasks"}
  ]
})
def list_tasks():
    user = current_user()
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 10)), 1), 100)
    completed = request.args.get("completed")
    completed_filter = None if completed is None else (completed.lower() in ["1", "true", "yes"])

    q = Task.query
    if not is_admin() or request.args.get("all") not in ("1", "true", "yes"):
        q = q.filter(Task.owner_id == user.id)

    if completed_filter is not None:
        q = q.filter(Task.completed == completed_filter)

    pagination = q.order_by(Task.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": out_list_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }

@tasks_bp.get("/<int:task_id>")
@jwt_required()
@swag_from({"tags": ["Tasks"], "summary": "Get a task by id"})
def get_task(task_id: int):
    user = current_user()
    task = Task.query.get_or_404(task_id)
    if not is_admin() and task.owner_id != user.id:
        return {"message": "Not found"}, 404
    return out_schema.dump(task)

@tasks_bp.post("/")
@jwt_required()
@swag_from({"tags": ["Tasks"], "summary": "Create a task"})
def create_task():
    user = current_user()
    payload = request.get_json() or {}
    data = create_schema.load(payload)
    task = Task(owner_id=user.id, **data)
    db.session.add(task)
    db.session.commit()
    return out_schema.dump(task), 201

@tasks_bp.put("/<int:task_id>")
@jwt_required()
@swag_from({"tags": ["Tasks"], "summary": "Update a task"})
def update_task(task_id: int):
    user = current_user()
    task = Task.query.get_or_404(task_id)
    if not is_admin() and task.owner_id != user.id:
        return {"message": "Not found"}, 404
    payload = request.get_json() or {}
    data = update_schema.load(payload)
    for k, v in data.items():
        setattr(task, k, v)
    db.session.commit()
    return out_schema.dump(task)

@tasks_bp.delete("/<int:task_id>")
@jwt_required()
@swag_from({"tags": ["Tasks"], "summary": "Delete a task"})
def delete_task(task_id: int):
    user = current_user()
    task = Task.query.get_or_404(task_id)
    if not is_admin() and task.owner_id != user.id:
        return {"message": "Not found"}, 404
    db.session.delete(task)
    db.session.commit()
    return {"message": "Deleted"}, 204
