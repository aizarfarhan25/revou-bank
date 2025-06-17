import pytest
from decimal import Decimal
from models.account import Account
from models.user import User

@pytest.fixture
def test_user(db_session):
    """Fixture to create test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        password="TestPass123!",
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    db_session.commit()
    return user

class TestAccount:
    """Test suite for Account model"""

    def test_create_account(self, db_session, test_user):
        """Test account creation"""
        account = Account(
            user_id=test_user.user_id,
            account_type="savings",
            account_number="TEST-ACC-001",
            balance=1000.00
        )
        db_session.add(account)
        db_session.commit()

        assert account.account_id is not None
        assert account.balance == Decimal('1000.00')

    def test_update_balance(self, db_session, test_user):
        """Test balance update functionality"""
        account = Account(
            user_id=test_user.user_id,
            account_type="savings",
            account_number="TEST-ACC-001",
            balance=1000.00
        )
        db_session.add(account)
        db_session.commit()

        account.update_balance(500.00)
        assert account.balance == Decimal('1500.00')

        account.update_balance(-200.00)
        assert account.balance == Decimal('1300.00')