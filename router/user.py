from flask import Blueprint, jsonify, request
from repo.user import get_all_user, create_new_user, get_user_by_id_db, update_existing_user as updated_selected_user , delete_user
from pydantic import BaseModel, ValidationError

class UserRequest(BaseModel):
    user_email: str
    username: str
    user_password: str
    first_name: str
    last_name: str
    # full_name: str

user_router = Blueprint("user_router", __name__, url_prefix="/api/v1/users")

        
@user_router.route("", methods=["GET"])
def get_user():
    users = get_all_user()
    return jsonify({"data": users}), 200


@user_router.route("/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """Get user by ID endpoint"""
    try:
        user = get_user_by_id_db(user_id)
        
        if not user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": {
                "user_id": user.user_id,
                "username": user.username,
                "user_email": user.user_email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        

@user_router.route("", methods=["POST"])
def create_user():
    data = request.json
    try:
        user = UserRequest.model_validate(data)
    except ValidationError as e:
        return jsonify(
            {
                "success": False,
                "data": e.errors(include_url=False, include_context=False, include_input=False),
            }
        ), 400
    created_user = create_new_user(
        user.user_email, user.username, user.user_password, user.first_name, user.last_name
    )
    return jsonify(
        {
            "data": {
                "user_email": created_user.user_email,
                "user_id": created_user.user_id,
            },
            "success": True
        }
    ), 201
    

@user_router.route("/<user_id>", methods=["PUT"])
def update_existing_user(user_id):
    try:
        data = request.json
        updated_user = updated_selected_user(user_id, data)
        
        if not updated_user:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": updated_user.obj_to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        
        
@user_router.route("/<user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    try:
        result = delete_user(user_id)
        
        if not result:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "User deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500