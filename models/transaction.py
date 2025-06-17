from datetime import datetime
from utils.database import db
from sqlalchemy.types import Numeric
from decimal import Decimal


class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.String(10), primary_key=True)  # TRX000001
    user_id = db.Column(db.String(5), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    from_account_id = db.Column(db.String(5), db.ForeignKey('accounts.account_id'), nullable=False)
    to_account_id = db.Column(db.String(5), db.ForeignKey('accounts.account_id'), nullable=True)  # Nullable for withdrawals
    amount = db.Column(Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdraw, transfer
    balance_before = db.Column(Numeric(10, 2), nullable=False)
    balance_after = db.Column(Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    @classmethod
    def generate_transaction_id(cls):
        last_transaction = cls.query.order_by(cls.transaction_id.desc()).first()
        
        if not last_transaction:
            return 'TR001'
            
        last_number = int(last_transaction.transaction_id[2:])
        next_number = last_number + 1
        
        return f'TR{next_number:03d}'

    def __init__(self, user_id, from_account_id, amount, transaction_type, balance_before, balance_after, description=None, to_account_id=None):
        self.transaction_id = self.generate_transaction_id()
        self.user_id = user_id
        self.from_account_id = from_account_id
        self.to_account_id = to_account_id
        self.amount = Decimal(str(amount))
        self.transaction_type = transaction_type
        self.balance_before = Decimal(str(balance_before))
        self.balance_after = Decimal(str(balance_after))
        self.description = description
        

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'from_account_id': self.from_account_id,
            'to_account_id': self.to_account_id,
            'amount': float(self.amount),
            'transaction_type': self.transaction_type,
            'balance_before': float(self.balance_before),
            'balance_after': float(self.balance_after),
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
