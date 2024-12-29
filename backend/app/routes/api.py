# app/routes/api.py
from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/test')
def test():
    return jsonify({"message": "Backend is working!"})