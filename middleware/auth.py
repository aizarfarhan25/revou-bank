# from flask import request
# from auth.login import claim_user

# def auth_middleware():
#     """Middleware to authenticate requests using Authorization header"""
#     auth_header = request.headers.get('Authorization')
    
#     if auth_header and auth_header.startswith('Bearer '):
#         token = auth_header.split(' ')[1]
#         try:
#             user = claim_user(token)
#             # Simpan user di request object
#             request.user = user
#         except Exception as e:
#             # Token tidak valid, biarkan request.user tetap None
#             pass


from flask import request, jsonify
from auth.login import claim_user

def auth_middleware():
    if request.endpoint == 'auth_router.login':
        return

    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return jsonify({
            "success": False,
            "message": "No authorization header"
        }), 401
    
    if not auth_header.startswith('Bearer '):
        return jsonify({
            "success": False,
            "message": "Invalid authorization format"
        }), 401

    try:
        token = auth_header.split(' ')[1]
        user = claim_user(token)
        
        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid or expired token"
            }), 401
            
        request.user = user
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Authentication failed: {str(e)}"
        }), 401
