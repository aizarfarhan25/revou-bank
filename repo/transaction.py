from datetime import datetime
import copy
from models.transaction import dummy_transactions

def create_transaction(data: dict) -> dict:
    transaction_ids = list(dummy_transactions["transactions"].keys())
    new_id = max(transaction_ids) + 1 if transaction_ids else 1
    
    transaction = {
        "transaction_number": f"TRX{new_id:03d}",
        **data,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }
    
    dummy_transactions["transactions"][new_id] = transaction
    return transaction

def get_account_transactions(account_id: int, start_date=None, end_date=None) -> list:
    transactions = []
    for trx in dummy_transactions["transactions"].values():
        if trx["account_id"] == account_id:
            if start_date and trx["timestamp"] < start_date:
                continue
            if end_date and trx["timestamp"] > end_date:
                continue
            transactions.append(copy.deepcopy(trx))
    return sorted(transactions, key=lambda x: x["timestamp"], reverse=True)