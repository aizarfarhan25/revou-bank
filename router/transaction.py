from flask import Blueprint, jsonify, request
from auth.login import login_required
from repo.transaction import (
    process_deposit, process_withdrawal, process_transfer,
    get_all_transactions, get_user_transactions, get_account_transactions
)
from pydantic import BaseModel, Field

transaction_router = Blueprint("transaction_router", __name__, url_prefix="/api/v1/transactions")

class TransactionBase(BaseModel):
    amount: float = Field(gt=0)
    description: str | None = None

class DepositRequest(TransactionBase):
    account_number: str

class WithdrawRequest(TransactionBase):
    account_number: str

class TransferRequest(TransactionBase):
    from_account_number: str
    to_account_number: str
    
@transaction_router.route("/deposit", methods=["POST"])
@login_required
def deposit():
    try:

        data = DepositRequest.model_validate(request.json)
        user = request.user
        print(user)

        
        # Process deposit
        transaction = process_deposit(
            data.account_number,
            user['user_id'],
            data.amount,
            data.description
        )
        
        return jsonify({
            "success": True,
            "data": transaction.to_dict()
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

@transaction_router.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    try:
        data = WithdrawRequest.model_validate(request.json)
        user = request.user
        
        transaction = process_withdrawal(
            data.account_number,
            user['user_id'],
            data.amount,
            data.description
        )
        
        return jsonify({
            "success": True,
            "data": transaction.to_dict()
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

@transaction_router.route("/transfer", methods=["POST"])
@login_required
def transfer():
    try:
        data = TransferRequest.model_validate(request.json)
        user = request.user
        
        transaction = process_transfer(
            data.from_account_number,
            data.to_account_number,
            user['user_id'],
            data.amount,
            data.description
        )
        
        return jsonify({
            "success": True,
            "data": transaction.to_dict()
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

@transaction_router.route("", methods=["GET"])
@login_required
def get_transactions():
    """Get all transactions (admin only)"""
    try:
        transactions = get_all_transactions()
        return jsonify({
            "success": True,
            "data": [t.to_dict() for t in transactions]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@transaction_router.route("/user/<user_id>", methods=["GET"])
@login_required
def get_user_transaction_history(user_id):
    try:
        transactions = get_user_transactions(user_id)
        return jsonify({
            "success": True,
            "data": [t.to_dict() for t in transactions]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@transaction_router.route("/account/<account_id>", methods=["GET"])
@login_required
def get_account_transaction_history(account_id):
    try:
        transactions = get_account_transactions(account_id)
        return jsonify({
            "success": True,
            "data": [t.to_dict() for t in transactions]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
