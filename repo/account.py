from utils.database import db
from models.account import Account
from decimal import Decimal


def create_new_account(user_id: str, account_type: str, balance: float = 0.00):
    try:
        account = Account(
            user_id=user_id,
            account_type=account_type,
            balance=balance
        )
        db.session.add(account)
        db.session.commit()
        return account
    except Exception as e:
        db.session.rollback()
        raise e

# ini untuk get all account    
def get_all_accounts():
    try:
        accounts = Account.query.all()
        return accounts
    except Exception as e:
        raise e

# ini untuk get account by user_id      
def get_user_accounts(user_id: str):
    try:
        accounts = Account.query.filter_by(user_id=user_id).all()
        return accounts
    except Exception as e:
        raise e

# ini untuk get account by ID    
def get_account_by_id(account_id: str):
    try:
        account = Account.query.filter_by(account_id=account_id).first()
        return account
    except Exception as e:
        raise e

# ini untuk delete account    
def delete_account(account_id: str):
    try:
        account = Account.query.filter_by(account_id=account_id).first()
        if not account:
            return None
            
        # cek saldo
        if account.balance > 0:
            raise ValueError("Cannot delete account with positive balance")
            
        db.session.delete(account)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e