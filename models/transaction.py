dummy_transactions = {
    "transactions": {
        1: {
            "transaction_number": "TRX001",
            "account_id": 1,
            "type": "deposit", 
            "amount": 50000,
            "balance_before": 950000,
            "balance_after": 1000000,
            "description": "Initial deposit",
            "timestamp": "2024-03-09T10:00:00",
            "to_account_id": None,
            "status": "success"
        },
        2: {
            "transaction_number": "TRX002",
            "account_id": 2,
            "type": "withdrawal",
            "amount": 25000,
            "balance_before": 525000,
            "balance_after": 500000,
            "description": "ATM withdrawal",
            "timestamp": "2024-03-09T11:30:00",
            "to_account_id": None,
            "status": "success"
        }
    }
}