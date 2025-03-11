from datetime import datetime
import copy
from models.account import dummy_accounts

def create_account(user_id: int) -> dict:
    account_ids = list(dummy_accounts["accounts"].keys())
    new_id = max(account_ids) + 1 if account_ids else 1
    
    account_data = {
        "account_number": f"ACC{new_id:03d}",
        "user_id": user_id,
        "balance": 0,
        "type": "savings",
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    dummy_accounts["accounts"][new_id] = account_data
    return account_data

def get_specific_account(account_id: int, user_id: int) -> dict:
    if account_id in dummy_accounts["accounts"]:
        account = dummy_accounts["accounts"][account_id]
        if account["user_id"] == user_id:
            account_copy = copy.deepcopy(account)
            account_copy["id"] = account_id
            return account_copy
    return None

def list_user_accounts(user_id: int) -> list:
    user_accounts = []
    for acc_id, account in dummy_accounts["accounts"].items():
        if account["user_id"] == user_id:
            acc_copy = copy.deepcopy(account)
            acc_copy["id"] = acc_id
            user_accounts.append(acc_copy)
    return user_accounts

def update_balance(account_id: int, amount: float) -> bool:
    if account_id in dummy_accounts["accounts"]:
        dummy_accounts["accounts"][account_id]["balance"] += amount
        return True
    return False

def delete_account(account_id: int) -> bool:
    if account_id in dummy_accounts["accounts"]:
        account = dummy_accounts["accounts"][account_id]
        if account["balance"] > 0:
            return False
        dummy_accounts["accounts"].pop(account_id)
        return True
    return False