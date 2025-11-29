from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime
from .models import db, User


def hash_password(password):
    """Hash a password using werkzeug's security module"""
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)


def create_user(username, password, email=None, role_id=None):
    """Create a new user with hashed password"""
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return None, "Username already exists"
    
    if email and User.query.filter_by(email=email).first():
        return None, "Email already exists"
    
    # Create new user
    user = User(
        username=username,
        password_hash=hash_password(password),
        email=email,
        role_id=role_id,
        is_active=True
    )
    
    try:
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def authenticate_user(username, password):
    """Authenticate a user and return user object if successful"""
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return None, "Invalid username or password"
    
    if not user.is_active:
        return None, "User account is inactive"
    
    if not verify_password(user.password_hash, password):
        return None, "Invalid username or password"
    
    # Update last login
    user.last_login = datetime.utcnow()
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
    
    return user, None


def generate_tokens(user):
    """Generate access and refresh tokens for a user"""
    identity = str(user.id)
    additional_claims = {
        'username': user.username,
        'role_id': user.role_id
    }
    
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)
    
    return access_token, refresh_token

