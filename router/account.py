from flask import Blueprint, jsonify, request
from repo.account import create_new_account, get_account_by_id, get_user_accounts, get_all_accounts, delete_account
from pydantic import BaseModel, ValidationError


class AccountRequest(BaseModel):
    user_id: str
    account_type: str
    # account_number: str
    balance: float = 0.00

account_router = Blueprint("account_router", __name__, url_prefix="/api/v1/accounts")

# ini untuk create account
@account_router.route("", methods=["POST"])
def create_account():
    data = request.json
    try:
        account_data = AccountRequest.model_validate(data)
        created_account = create_new_account(
            account_data.user_id,
            account_data.account_type,
            account_data.balance
        )
        return jsonify({
            "success": True,
            "data": created_account.to_dict()
        }), 201
    except ValidationError as e:
        return jsonify({
            "success": False,
            "data": e.errors(include_url=False, include_context=False, include_input=False)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
       
# ini untuk get all account        
@account_router.route("", methods=["GET"])
def get_accounts():
    try:
        accounts = get_all_accounts()
        return jsonify({
            "success": True,
            "data": [account.to_dict() for account in accounts]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
 
# ini untk get account by account_id        
@account_router.route("/<account_id>", methods=["GET"])
def get_account(account_id):
    try:
        account = get_account_by_id(account_id)
        if not account:
            return jsonify({
                "success": False,
                "message": "Account not found"
            }), 404
        return jsonify({
            "success": True,
            "data": account.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        
        
# ini untuk get account by user_id       
@account_router.route("/user/<user_id>", methods=["GET"])
def list_accounts(user_id):
    try:
        accounts = get_user_accounts(user_id)
        return jsonify({
            "success": True,
            "data": [account.to_dict() for account in accounts]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# ini unrtu delete account        
@account_router.route("/<account_id>", methods=["DELETE"])
def delete_account_by_id(account_id):
    try:
        result = delete_account(account_id)
        
        if result is None:
            return jsonify({
                "success": False,
                "message": "Account not found"
            }), 404
            
        return jsonify({
            "success": True,
            "message": "Account deleted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500