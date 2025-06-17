# from flask import jsonify
# from repo.account import get_specific_account, update_balance
# from repo.transaction import create_transaction, get_account_transactions


from flask import jsonify
from repo.account import get_account_by_id
from repo.transaction import (
    process_deposit as deposit_transaction,
    process_withdrawal as withdraw_transaction,
    process_transfer as transfer_transaction,
    get_account_transactions
)
from decimal import Decimal


def process_deposit(account_id: str, user_id: str, amount: float, description: str):
    try:
        account = get_account_by_id(account_id)
        if not account:
            return jsonify({"message": "Account not found", "success": False}), 404

        if amount <= 0:
            return jsonify({"message": "Invalid amount", "success": False}), 400

        # deposit
        transaction = deposit_transaction(account_id, user_id, amount, description)
        
        return jsonify({
            "success": True,
            "data": transaction.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    

def process_withdrawal(account_id: str, user_id: str, amount: float, description: str):
    try:
        account = get_account_by_id(account_id)
        if not account:
            return jsonify({"message": "Account not found", "success": False}), 404

        if amount <= 0:
            return jsonify({"message": "Invalid amount", "success": False}), 400

        if account.balance < Decimal(str(amount)):
            return jsonify({"message": "Insufficient balance", "success": False}), 400

        #  withdrawal
        transaction = withdraw_transaction(account_id, user_id, amount, description)
        
        return jsonify({
            "success": True,
            "data": transaction.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    

def process_transfer(from_account_number: str, to_account_number: str, 
                    user_id: str, amount: float, description: str):
    try:
        if amount <= 0:
            return jsonify({"message": "Invalid amount", "success": False}), 400

        # transfer
        transaction = transfer_transaction(
            from_account_number,
            to_account_number,
            user_id,
            amount,
            description
        )
        
        return jsonify({
            "success": True,
            "data": transaction.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({"message": str(e), "success": False}), 400
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
    

def get_transaction_history(account_id: str, user_id: str, start_date=None, end_date=None):
    try:
        account = get_account_by_id(account_id)
        if not account:
            return jsonify({"message": "Account not found", "success": False}), 404

        # get transactions
        transactions = get_account_transactions(account_id)
        
        return jsonify({
            "success": True,
            "data": [t.to_dict() for t in transactions]
        }), 200
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500


# def process_deposit(account_id: int, user_id: int, amount: float, description: str):
#     try:
#         account = get_specific_account(account_id, user_id)
#         if not account:
#             return jsonify({"message": "Account not found", "success": False}), 404

#         if amount <= 0:
#             return jsonify({"message": "Invalid amount", "success": False}), 400

#         balance_before = account["balance"]
#         update_balance(account_id, amount)

#         transaction = create_transaction(
#             {
#                 "account_id": account_id,
#                 "type": "deposit",
#                 "amount": amount,
#                 "balance_before": balance_before,
#                 "balance_after": balance_before + amount,
#                 "description": description,
#                 "to_account_id": None
#             }
#         )

#         return jsonify({"data": transaction, "success": True}), 200
#     except Exception as e:
#         return jsonify({"message": str(e), "success": False}), 500


# def process_withdrawal(account_id: int, user_id: int, amount: float, description: str):
#     try:
#         account = get_specific_account(account_id, user_id)
#         if not account:
#             return jsonify({"message": "Account not found", "success": False}), 404

#         if amount <= 0:
#             return jsonify({"message": "Invalid amount", "success": False}), 400

#         if account["balance"] < amount:
#             return jsonify({"message": "Insufficient balance", "success": False}), 400

#         balance_before = account["balance"]
#         update_balance(account_id, -amount)

#         transaction = create_transaction(
#             {
#                 "account_id": account_id,
#                 "type": "withdrawal",
#                 "amount": amount,
#                 "balance_before": balance_before,
#                 "balance_after": balance_before - amount,
#                 "description": description,
#                 "to_account_id": None
#             }
#         )

#         return jsonify({"data": transaction, "success": True}), 200
#     except Exception as e:
#         return jsonify({"message": str(e), "success": False}), 500


# def process_transfer(
#     from_account_id: int,
#     to_account_id: int,
#     user_id: int,
#     amount: float,
#     description: str,
# ):
#     try:
#         # Validate source account
#         from_account = get_specific_account(from_account_id, user_id)
#         if not from_account:
#             return jsonify(
#                 {"message": "Source account not found", "success": False}
#             ), 404

#         # Validate destination account
#         to_account = get_specific_account(
#             to_account_id, None
#         )  # Allow transfer to any account
#         if not to_account:
#             return jsonify(
#                 {"message": "Destination account not found", "success": False}
#             ), 404

#         if amount <= 0:
#             return jsonify({"message": "Invalid amount", "success": False}), 400

#         if from_account["balance"] < amount:
#             return jsonify({"message": "Insufficient balance", "success": False}), 400

#         # Process withdrawal from source
#         from_balance = from_account["balance"]
#         update_balance(from_account_id, -amount)

#         # Process deposit to destination
#         to_balance = to_account["balance"]
#         update_balance(to_account_id, amount)

#         # Create transfer transaction
#         transaction = create_transaction(
#             {
#                 "account_id": from_account_id,
#                 "type": "transfer",
#                 "amount": amount,
#                 "balance_before": from_balance,
#                 "balance_after": from_balance - amount,
#                 "description": description,
#                 "to_account_id": to_account_id,
#             }
#         )

#         return jsonify({"data": transaction, "success": True}), 200
#     except Exception as e:
#         return jsonify({"message": str(e), "success": False}), 500


# def get_transaction_history(
#     account_id: int, user_id: int, start_date=None, end_date=None
# ):
#     try:
#         account = get_specific_account(account_id, user_id)
#         if not account:
#             return jsonify({"message": "Account not found", "success": False}), 404

#         transactions = get_account_transactions(account_id, start_date, end_date)
#         return jsonify({"data": transactions, "success": True}), 200
#     except Exception as e:
#         return jsonify({"message": str(e), "success": False}), 500
