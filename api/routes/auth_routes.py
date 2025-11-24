from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from ..models import db
from ..auth import create_user, authenticate_user, generate_tokens
from ..utils import error_response, success_response, validate_request_json

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    is_valid, missing = validate_request_json(['username', 'password'])
    if not is_valid:
        return error_response(f"Missing required fields: {', '.join(missing)}", 400)
    
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    email = data.get('email', '').strip() or None
    
    # Validate input
    if not username or len(username) < 3:
        return error_response("Username must be at least 3 characters", 400)
    
    if not password or len(password) < 6:
        return error_response("Password must be at least 6 characters", 400)
    
    # Create user
    user, error = create_user(username, password, email)
    if error:
        return error_response(error, 400)
    
    # Generate tokens
    access_token, refresh_token = generate_tokens(user)
    
    return success_response({
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }, "User registered successfully", 201)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    is_valid, missing = validate_request_json(['username', 'password'])
    if not is_valid:
        return error_response(f"Missing required fields: {', '.join(missing)}", 400)
    
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Authenticate user
    user, error = authenticate_user(username, password)
    if error:
        return error_response(error, 401)
    
    # Generate tokens
    access_token, refresh_token = generate_tokens(user)
    
    return success_response({
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }, "Login successful")


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    try:
        identity = get_jwt_identity()
        if identity and isinstance(identity, dict):
            # Create new access token
            access_token = create_access_token(identity=identity)
            return success_response({
                'access_token': access_token
            }, "Token refreshed successfully")
        else:
            return error_response("Invalid token identity", 401)
    except Exception as e:
        return error_response("Failed to refresh token", 401)


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """Get current authenticated user information"""
    from ..utils import get_current_user
    
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    return success_response({
        'user': user.to_dict(include_sensitive=True)
    })

