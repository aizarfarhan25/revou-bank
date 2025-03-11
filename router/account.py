from flask import Blueprint, request
from auth.login import login_required
from views.account import (
    create_user_account,
    get_account_detail,
    get_user_accounts,
    delete_user_account
)
from views.transaction import (
    process_deposit,
    process_withdrawal,
    get_transaction_history
)

account_router = Blueprint("account_router", __name__, url_prefix="/api/v1/accounts")

@account_router.route("", methods=["POST"])
@login_required
def create_account():
    user = getattr(request, "user")
    return create_user_account(user["id"])

@account_router.route("", methods=["GET"])
@login_required
def list_accounts():
    user = getattr(request, "user")
    return get_user_accounts(user["id"])

@account_router.route("/<int:account_id>", methods=["GET", "DELETE"])
@login_required
def handle_specific_account(account_id):
    user = getattr(request, "user")
    if request.method == "GET":
        return get_account_detail(account_id, user["id"])
    return delete_user_account(account_id, user["id"])

@account_router.route("/<int:account_id>/deposit", methods=["POST"])
@login_required
def deposit(account_id):
    user = getattr(request, "user")
    data = request.json
    amount = data.get("amount")
    description = data.get("description", "Deposit")
    return process_deposit(account_id, user["id"], amount, description)

@account_router.route("/<int:account_id>/withdraw", methods=["POST"])
@login_required
def withdraw(account_id):
    user = getattr(request, "user")
    data = request.json
    amount = data.get("amount")
    description = data.get("description", "Withdrawal")
    return process_withdrawal(account_id, user["id"], amount, description)

@account_router.route("/<int:account_id>/transactions", methods=["GET"])
@login_required
def transactions(account_id):
    user = getattr(request, "user")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    return get_transaction_history(account_id, user["id"], start_date, end_date)