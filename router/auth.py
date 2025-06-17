from flask import Blueprint, request, jsonify
from views.auth import user_login
from repo.user import find_user_by_email
from auth.login import get_token
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str


auth_router = Blueprint("auth_router", __name__, url_prefix="/api/v1/auth")


@auth_router.route('/login', methods=['POST'])
def login():
    try:
        data = LoginRequest.model_validate(request.json)
        user = find_user_by_email(data.email)
        
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401
            
        if not user.verify_password(data.password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401
            
        token = get_token(user)
        
        return jsonify({
            "success": True,
            "data": {
                "token": token,
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.user_email
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500