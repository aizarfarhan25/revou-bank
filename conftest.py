import pytest
from flask import Flask
from utils.database import db
from faker import Faker
from decimal import Decimal

@pytest.fixture
def app():
    """Create application for the tests."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.jvmdqyfqubsmdvfkanvi:Secret123-{}:@aws-0-ap-southeast-1.pooler.supabase.com/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    return app

@pytest.fixture
def db(app):
    """Database fixture"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def fake():
    return Faker()

@pytest.fixture
def sample_users(app, db):
    """Create sample users similar to SQL insert"""
    users = [
        {
            "username": "aizarfarhan25",
            "email": "aizar@gmail.com",
            "password": "TestPass123!",
            "first_name": "Aizar",
            "last_name": "Farhan"
        },
        {
            "username": "yanto_gantenk",
            "email": "yanktonk@gmail.com",
            "password": "TestPass123!",
            "first_name": "Yanto",
            "last_name": "Suranto"
        },
        {
            "username": "natdcoco",
            "email": "natadcoco@gmail.com",
            "password": "TestPass123!",
            "first_name": "Nata",
            "last_name": "Decoco"
        }
    ]
    
    from models.user import User
    user_objects = []
    for user_data in users:
        user = User(**user_data)
        user_objects.append(user)
    
    db.session.add_all(user_objects)
    db.session.commit()
    
    return user_objects

@pytest.fixture
def sample_accounts(app, db, sample_users):
    """Create sample accounts similar to SQL insert"""
    accounts = [
        {
            "user_id": sample_users[0].user_id,
            "account_type": "Tabungan",
            "account_number": "ACC001",
            "balance": Decimal('1000000.00')
        },
        {
            "user_id": sample_users[0].user_id,
            "account_type": "Giro",
            "account_number": "ACC002",
            "balance": Decimal('5000000.00')
        },
        {
            "user_id": sample_users[1].user_id,
            "account_type": "Tabungan",
            "account_number": "ACC003",
            "balance": Decimal('0.00')
        }
    ]
    
    from models.account import Account
    account_objects = []
    for account_data in accounts:
        account = Account(**account_data)
        account_objects.append(account)
    
    db.session.add_all(account_objects)
    db.session.commit()
    
    return account_objects

@pytest.fixture
def client(app):
    return app.test_client()