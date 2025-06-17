from datetime import datetime
from utils.database import db
from sqlalchemy.types import Numeric
from decimal import Decimal
from uuid import uuid4
import random

class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.String(5), primary_key=True)
    user_id = db.Column(db.String(5), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), unique=True, nullable=False)
    balance = db.Column(Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    @classmethod
    def generate_account_id(cls):
        last_account = cls.query.order_by(cls.account_id.desc()).first()
        
        if not last_account:
            return 'AC001'
            
        last_number = int(last_account.account_id[2:])
        next_number = last_number + 1
        
        return f'AC{next_number:03d}'

    @staticmethod
    def generate_account_number():
        return str(random.randint(1000000, 9999999))

    def __init__(self, user_id, account_type, balance=0.00):
        self.account_id = self.generate_account_id()
        self.user_id = user_id
        self.account_type = account_type
        self.account_number = self.generate_account_number()
        self.balance = Decimal(str(balance))

    def update_balance(self, amount):
        try:
            self.balance += Decimal(str(amount))
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_type': self.account_type,
            'account_number': self.account_number,
            'balance': float(self.balance),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }