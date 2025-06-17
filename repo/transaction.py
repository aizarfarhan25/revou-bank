from utils.database import db
from models.transaction import Transaction
from models.account import Account
from decimal import Decimal
from sqlalchemy import and_, or_


def create_transaction(user_id: str, from_account_id: str, amount: float, 
                      transaction_type: str, balance_before: float, 
                      balance_after: float, description: str = None, 
                      to_account_id: str = None):
    try:
        transaction = Transaction(
            user_id=user_id,
            from_account_id=from_account_id,
            amount=amount,
            transaction_type=transaction_type,
            balance_before=balance_before,
            balance_after=balance_after,
            description=description,
            to_account_id=to_account_id
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        raise e
    

# untuk get all transactions
def get_all_transactions():
    return Transaction.query.order_by(Transaction.created_at.desc()).all()


# untuk get transactions dari specific user
def get_user_transactions(user_id: str):
    return Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()


# untuk get transactions dari specific account
def get_account_transactions(account_id: str):
    return Transaction.query.filter(
        or_(
            Transaction.from_account_id == account_id,
            Transaction.to_account_id == account_id
        )
    ).order_by(Transaction.created_at.desc()).all()


# deposit / setor tunai
def process_deposit(account_number: str, user_id: str, amount: float, description: str = None):
    try:

        account = Account.query.filter_by(account_number=account_number, user_id=user_id).first() 
        if not account:

            raise ValueError(f"Account {account_number} not found")
             
        balance_before = float(account.balance)
        account.balance += Decimal(str(amount))       
        transaction = Transaction(
            user_id=user_id,
            from_account_id=account.account_id,
            amount=amount,
            transaction_type="deposit",
            balance_before=balance_before,
            balance_after=float(account.balance),
            description=description
        )
        
        db.session.add(transaction)
        db.session.commit()
        return transaction
        
    except Exception as e:
        db.session.rollback()
        raise e


# withdraw / tarik tubnai    
def process_withdrawal(account_number: str, user_id: str, amount: float, description: str = None):
    try:
        account = Account.query.filter_by(account_number=account_number, user_id=user_id).first()
        if not account:
            raise ValueError("Account not found")
            
        if account.balance < Decimal(str(amount)):
            raise ValueError("Insufficient balance")
            
        balance_before = float(account.balance)
        account.balance -= Decimal(str(amount))    
        transaction = create_transaction(
            user_id=user_id,
            from_account_id=account.account_id,
            amount=amount,
            transaction_type="withdrawal",
            balance_before=balance_before,
            balance_after=float(account.balance),
            description=description
        )
        
        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        raise e


# transfer
def process_transfer(from_account_number: str, to_account_number: str, user_id: str, amount: float, description: str = None):
    try:
        from_account = Account.query.filter_by(account_number=from_account_number, user_id=user_id).first()
        to_account = Account.query.filter_by(account_number=to_account_number).first()
        
        if not from_account or not to_account:
            raise ValueError("One or both accounts not found")
            
        if from_account.balance < Decimal(str(amount)):
            raise ValueError("Insufficient balance")
            
        # Process transfer
        from_balance_before = float(from_account.balance)
        to_balance_before = float(to_account.balance)
        
        from_account.balance -= Decimal(str(amount))
        to_account.balance += Decimal(str(amount))
        
        transaction = create_transaction(
            user_id=user_id,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
            amount=amount,
            transaction_type="transfer",
            balance_before=from_balance_before,
            balance_after=float(from_account.balance),
            description=description
        )
        
        db.session.commit()
        return transaction
    except Exception as e:
        db.session.rollback()
        raise e