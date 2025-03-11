from flask import Blueprint, request
from auth.login import login_required
from views.transaction import (
    process_deposit,
    process_withdrawal,
    process_transfer,
    get_transaction_history
)

transaction_router = Blueprint("transaction_router", __name__, url_prefix="/api/v1/transactions")

@transaction_router.route("/deposit", methods=["POST"]) 
@login_required
def deposit():
    user = getattr(request, "user")
    data = request.json
    account_id = data.get("account_id")
    amount = data.get("amount")
    description = data.get("description", "Deposit")
    
    return process_deposit(account_id, user["id"], amount, description)

@transaction_router.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    user = getattr(request, "user")
    data = request.json
    account_id = data.get("account_id")
    amount = data.get("amount")
    description = data.get("description", "Withdrawal")
    
    return process_withdrawal(account_id, user["id"], amount, description)

@transaction_router.route("/transfer", methods=["POST"])
@login_required
def transfer():
    user = getattr(request, "user")
    data = request.json
    from_account_id = data.get("from_account_id")
    to_account_id = data.get("to_account_id")
    amount = data.get("amount")
    description = data.get("description", "Transfer")
    
    return process_transfer(from_account_id, to_account_id, user["id"], amount, description)

@transaction_router.route("/history/<int:account_id>", methods=["GET"])
@login_required
def history(account_id):
    user = getattr(request, "user")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    # sort_by = request.args.get("sort_by", "timestamp")  # Default sort by timestamp
    # sort_order = request.args.get("sort_order", "desc")  # Default descending
    
    return get_transaction_history(
        account_id, 
        user["id"], 
        start_date, 
        end_date
    )