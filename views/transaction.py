from flask import jsonify
from repo.account import get_specific_account, update_balance
from repo.transaction import create_transaction, get_account_transactions


def process_deposit(account_id: int, user_id: int, amount: float, description: str):
    try:
        account = get_specific_account(account_id, user_id)
        if not account:
            return jsonify({"message": "Account not found", "success": False}), 404

        if amount <= 0:
            return jsonify({"message": "Invalid amount", "success": False}), 400

        balance_before = account["balance"]
        update_balance(account_id, amount)

        transaction = create_transaction(
            {
                "account_id": account_id,
                "type": "deposit",
                "amount": amount,
                "balance_before": balance_before,
                "balance_after": balance_before + amount,
                "description": description,
            }
        )

        return jsonify({"data": transaction, "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


def process_withdrawal(account_id: int, user_id: int, amount: float, description: str):
    try:
        account = get_specific_account(account_id, user_id)
        if not account:
            return jsonify({"message": "Account not found", "success": False}), 404

        if amount <= 0:
            return jsonify({"message": "Invalid amount", "success": False}), 400

        if account["balance"] < amount:
            return jsonify({"message": "Insufficient balance", "success": False}), 400

        balance_before = account["balance"]
        update_balance(account_id, -amount)

        transaction = create_transaction(
            {
                "account_id": account_id,
                "type": "withdrawal",
                "amount": amount,
                "balance_before": balance_before,
                "balance_after": balance_before - amount,
                "description": description,
            }
        )

        return jsonify({"data": transaction, "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


def process_transfer(
    from_account_id: int,
    to_account_id: int,
    user_id: int,
    amount: float,
    description: str,
):
    try:
        # Validate source account
        from_account = get_specific_account(from_account_id, user_id)
        if not from_account:
            return jsonify(
                {"message": "Source account not found", "success": False}
            ), 404

        # Validate destination account
        to_account = get_specific_account(
            to_account_id, None
        )  # Allow transfer to any account
        if not to_account:
            return jsonify(
                {"message": "Destination account not found", "success": False}
            ), 404

        if amount <= 0:
            return jsonify({"message": "Invalid amount", "success": False}), 400

        if from_account["balance"] < amount:
            return jsonify({"message": "Insufficient balance", "success": False}), 400

        # Process withdrawal from source
        from_balance = from_account["balance"]
        update_balance(from_account_id, -amount)

        # Process deposit to destination
        update_balance(to_account_id, amount)

        # Create transfer transaction
        transaction = create_transaction(
            {
                "account_id": from_account_id,
                "type": "transfer",
                "amount": amount,
                "balance_before": from_balance,
                "balance_after": from_balance - amount,
                "description": description,
                "to_account_id": to_account_id,
            }
        )

        return jsonify({"data": transaction, "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


def get_transaction_history(
    account_id: int, user_id: int, start_date=None, end_date=None
):
    try:
        account = get_specific_account(account_id, user_id)
        if not account:
            return jsonify({"message": "Account not found", "success": False}), 404

        transactions = get_account_transactions(account_id, start_date, end_date)
        return jsonify({"data": transactions, "success": True}), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
