import pytest
from models.user import User, PasswordError

class TestUser:
    """Test suite for User model"""

    def test_create_user(self, app, db):  # Changed from db_session to app, db
        """Test basic user creation"""
        user = User(
            username="testuser",
            email="test@example.com",
            password="TestPass123!", 
            first_name="Test",
            last_name="User"
        )
        db.session.add(user)
        db.session.commit()

        assert user.user_id is not None
        assert user.username == "testuser"
        assert user.full_name == "Test User"

    def test_create_user_with_sample_data(self, app, db, sample_users):  # Changed from db_session
        """Test user creation with sample data"""
        user = sample_users[0]
        assert user.username == "aizarfarhan25"
        assert user.user_email == "aizar@gmail.com"
        assert user.full_name == "Aizar Farhan"

    def test_password_validation(self):
        """Test password validation rules"""
        with pytest.raises(PasswordError):
            User.validate_password("short")
        
        with pytest.raises(PasswordError):
            User.validate_password("nouppercase123!")
        
        assert User.validate_password("TestPass123!") is True

    def test_user_account_relationship(self, app, db, sample_users, sample_accounts):  # Changed from db_session
        """Test user-account relationship"""
        user = sample_users[0]  # aizarfarhan25
        assert len(user.accounts) == 2  # Should have 2 accounts
        assert user.accounts[0].account_number == "ACC001"
        assert user.accounts[1].account_number == "ACC002"