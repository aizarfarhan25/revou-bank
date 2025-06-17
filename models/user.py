from datetime import datetime
from uuid import uuid4
from utils.database import db
import re
import bcrypt


class User(db.Model):
    __tablename__='users'
    user_id = db.Column(db.String(10), primary_key=True) 
    username = db.Column(db.String(255), unique=True)
    user_email = db.Column(db.String(255), unique=True)
    user_password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    full_name = db.Column(db.String(255), nullable=True)
    created_at =  db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<User {self.user_id}>'
    
    @classmethod
    def generate_user_id(cls):
        last_user = cls.query.order_by(cls.user_id.desc()).first()
        
        if not last_user:
            return 'US001'
            
        last_number = int(last_user.user_id[2:])
        next_number = last_number + 1
        
        return f'US{next_number:03d}'
    
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), 
                            self.user_password.encode('utf-8'))
    
    def __init__(self, email, password, username, first_name, last_name, full_name=None):
        self.user_id = self.generate_user_id()
        self.user_email = email
        self.username = username
        self.user_password = self.hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name or f"{first_name} {last_name}"

    def obj_to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


