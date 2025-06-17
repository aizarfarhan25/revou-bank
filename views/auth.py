from auth.login import get_token
from repo.user import find_user_by_email


def user_login(email, password):
    """
    Authenticate user and generate token
    """
    user = find_user_by_email(email)
    if not user:
        raise AssertionError("User not found")
    
    if user["password"] != password:
        raise AssertionError("Invalid password")
    
    # Add id to user data for token generation
    user_data = {**user, "id": user.get("id", 0)}
    token = get_token(user_data)
    
    return token
