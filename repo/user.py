from utils.database import db
from models.user import User

# get user by email
def find_user_by_email(email: str):
    try:
        user = User.query.filter_by(user_email=email).first()
        return user
    except Exception as e:
        raise e



# get all user
def get_all_user ():
    users = User.query.all()
    datas = [user.obj_to_dict() for user in users]
    return datas


# get user by ID
def get_user_by_id_db(user_id: str):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        return user
    except Exception as e:
        raise e

def create_new_user (user_email, username, user_password, first_name, last_name):
    user_item = User(
        email=user_email,
        username=username,
        password=user_password,
        first_name=first_name,
        last_name=last_name
        # full_name=full_name
    )
    db.session.add(user_item)
    db.session.commit()
    return user_item


# update existing user
def update_existing_user(user_id: str, user_data: dict):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return None
        
        if 'username' in user_data:
            user.username = user_data['username']
        if 'user_email' in user_data:
            user.user_email = user_data['user_email']
        if 'user_password' in user_data:
            user.user_password = user_data['user_password']
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
            user.full_name = f"{user.first_name} {user.last_name}"
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
            user.full_name = f"{user.first_name} {user.last_name}"
            
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e


# delete user    
def delete_user(user_id: str):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return None
        
        db.session.delete(user)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e
    
