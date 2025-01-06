# app/routes/sample_routes.py
from flask import Blueprint, jsonify

sample_bp = Blueprint('sample', __name__, url_prefix='/api/sample')

@sample_bp.route('/')
def test():
    return jsonify({"message": "Backend is working!"})