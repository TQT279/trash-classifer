import os
import uuid
from werkzeug.utils import secure_filename
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from .models import db, User


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        from .config import Config
        allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file to server
    Args:
        file: FileStorage object from request
        upload_folder: Directory to save the file
    Returns:
        tuple: (file_path, original_name) or (None, None) if error
    """
    try:
        if file and file.filename:
            # Check if file extension is allowed
            if not allowed_file(file.filename):
                return None, None
            
            # Generate unique filename
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
            
            # Ensure upload folder exists
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            return file_path, filename
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None, None
    
    return None, None


def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0


def get_mime_type(filename):
    """Get MIME type from filename"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp'
    }
    return mime_types.get(ext, 'application/octet-stream')


def get_current_user():
    """Get current authenticated user from JWT token"""
    try:
        identity = get_jwt_identity()
        if identity:
            try:
                user_id = int(identity)
            except (TypeError, ValueError):
                user_id = identity
            if user_id:
                return User.query.get(user_id)
    except Exception:
        pass
    return None


def error_response(message, status_code=400, error_code=None):
    """Create standardized error response"""
    response = {
        'success': False,
        'error': {
            'message': message
        }
    }
    if error_code:
        response['error']['code'] = error_code
    return jsonify(response), status_code


def success_response(data=None, message=None, status_code=200):
    """Create standardized success response"""
    response = {
        'success': True
    }
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code


def paginate_query(query, page=1, per_page=20):
    """
    Paginate a SQLAlchemy query
    Args:
        query: SQLAlchemy query object
        page: Page number (1-indexed)
        per_page: Items per page
    Returns:
        tuple: (paginated_items, total_count, total_pages)
    """
    try:
        page = max(1, int(page))
        per_page = max(1, min(100, int(per_page)))  # Limit to 100 per page
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    except Exception as e:
        return {
            'items': [],
            'total': 0,
            'page': 1,
            'per_page': per_page,
            'pages': 0,
            'has_next': False,
            'has_prev': False
        }


def validate_request_json(required_fields):
    """
    Validate that required fields are present in request JSON
    Args:
        required_fields: List of required field names
    Returns:
        tuple: (is_valid, missing_fields)
    """
    if not request.is_json:
        return False, ["Request must be JSON"]
    
    data = request.get_json()
    missing = [field for field in required_fields if field not in data or data[field] is None]
    
    return len(missing) == 0, missing

