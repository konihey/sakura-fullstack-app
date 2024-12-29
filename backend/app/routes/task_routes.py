# app/routes/task_routes.py
from flask import Blueprint, jsonify, request
from app.models.task import Task
from app import db

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')

@task_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(
        title=data['title'],
        description=data.get('description'),
        user_id=data['user_id']
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    task = Task.query.get_or_404(task_id)
    task.status = data['status']
    db.session.commit()
    return jsonify(task.to_dict())