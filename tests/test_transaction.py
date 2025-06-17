import pytest
from decimal import Decimal
from datetime import datetime
from models.transaction import Transaction
from models.account import Account
from models.user import User

@pytest.fixture
def setup_test_users(db_session):
    """Fixture to create test users"""
    users = [
        User(
            username="sender",
            email="sender@test.com",
            password="TestPass123!",
            first_name="Test",
            last_name="Sender"
        ),
        User(
            username="receiver",
            email="receiver@test.com",
            password="TestPass123!",
            first_name="Test",
            last_name="Receiver"
        )
    ]
    db_session.add_all(users)
    db_session.commit()
    return users

@pytest.fixture
def setup_test_accounts(db_session, setup_test_users):
    """Fixture to create test accounts"""
    accounts = [
        Account(
            user_id=setup_test_users[0].user_id,
            account_type="savings",
            account_number="TEST-ACC-001",
            balance=Decimal('1000.00')
        ),
        Account(
            user_id=setup_test_users[1].user_id,
            account_type="savings",
            account_number="TEST-ACC-002",
            balance=Decimal('500.00')
        )
    ]
    db_session.add_all(accounts)
    db_session.commit()
    return accounts

class TestTransaction:
    """Test suite for Transaction model"""

    def test_create_transaction(self, db_session, setup_test_accounts):
        """Test basic transaction creation"""
        from_account = setup_test_accounts[0]
        to_account = setup_test_accounts[1]
        
        transaction = Transaction(
            user_id=from_account.user_id,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
            amount=100.00,
            transaction_type="Transfer",
            description="Test transfer"
        )
        
        db_session.add(transaction)
        db_session.commit()
        
        assert transaction.transactions_id is not None
        assert transaction.amount == Decimal('100.00')
        assert transaction.transaction_type == "Transfer"

    def test_transaction_with_balance_update(self, db_session, setup_test_accounts):
        """Test transaction with balance updates"""
        from_account = setup_test_accounts[0]
        to_account = setup_test_accounts[1]
        initial_from_balance = from_account.balance
        initial_to_balance = to_account.balance
        
        # Create and process transaction
        transaction = Transaction.create_transaction(
            user_id=from_account.user_id,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
            amount=100.00,
            transaction_type="Transfer",
            description="Test transfer with balance update"
        )
        
        # Update balances
        from_account.update_balance(-100.00)
        to_account.update_balance(100.00)
        
        assert transaction.amount == Decimal('100.00')
        assert from_account.balance == initial_from_balance - Decimal('100.00')
        assert to_account.balance == initial_to_balance + Decimal('100.00')

    def test_invalid_transaction_amount(self, db_session, setup_test_accounts):
        """Test transaction with invalid amount"""
        from_account = setup_test_accounts[0]
        to_account = setup_test_accounts[1]
        
        with pytest.raises(ValueError):
            Transaction.create_transaction(
                user_id=from_account.user_id,
                from_account_id=from_account.account_id,
                to_account_id=to_account.account_id,
                amount=-100.00,  # Negative amount should raise error
                transaction_type="Transfer",
                description="Invalid transaction"
            )

    def test_transaction_timestamps(self, db_session, setup_test_accounts):
        """Test transaction timestamps are set correctly"""
        from_account = setup_test_accounts[0]
        to_account = setup_test_accounts[1]
        
        transaction = Transaction.create_transaction(
            user_id=from_account.user_id,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
            amount=100.00,
            transaction_type="Transfer",
            description="Test timestamps"
        )
        
        assert isinstance(transaction.created_at, datetime)
        assert transaction.created_at is not None

    def test_transaction_to_dict(self, db_session, setup_test_accounts):
        """Test transaction serialization to dictionary"""
        from_account = setup_test_accounts[0]
        to_account = setup_test_accounts[1]
        
        transaction = Transaction.create_transaction(
            user_id=from_account.user_id,
            from_account_id=from_account.account_id,
            to_account_id=to_account.account_id,
            amount=100.00,
            transaction_type="Transfer",
            description="Test serialization"
        )
        
        transaction_dict = transaction.to_dict()
        
        assert isinstance(transaction_dict, dict)
        assert transaction_dict['amount'] == float(transaction.amount)
        assert transaction_dict['transaction_type'] == transaction.transaction_type
        assert transaction_dict['description'] == transaction.description