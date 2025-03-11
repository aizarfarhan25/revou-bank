from flask import jsonify
from repo.account import (
    create_account,
    get_specific_account,
    list_user_accounts,
    delete_account
)

def create_user_account(user_id: int):
    try:
        account = create_account(user_id)
        return jsonify({
            "data": account,
            "success": True
        }), 201
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500

def get_account_detail(account_id: int, user_id: int):
    try:
        account = get_specific_account(account_id, user_id)
        if not account:
            return jsonify({
                "message": "Account not found or unauthorized",
                "success": False
            }), 404

        return jsonify({
            "data": account,
            "success": True
        }), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500

def get_user_accounts(user_id: int):
    try:
        accounts = list_user_accounts(user_id)
        return jsonify({
            "data": accounts,
            "success": True
        }), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500

def delete_user_account(account_id: int, user_id: int):
    try:
        account = get_specific_account(account_id, user_id)
        if not account:
            return jsonify({
                "message": "Account not found or unauthorized",
                "success": False
            }), 404
        
        if account["balance"] > 0:
            return jsonify({
                "message": "Cannot delete account with remaining balance",
                "success": False
            }), 400

        if delete_account(account_id):
            return jsonify({
                "message": "Account deleted successfully",
                "success": True
            }), 200
        return jsonify({
            "message": "Failed to delete account",
            "success": False
        }), 400
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500