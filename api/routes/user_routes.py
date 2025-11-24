from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from ..models import db, User, Image, ClassificationResult, Feedback
from ..utils import error_response, success_response, get_current_user, validate_request_json

user_bp = Blueprint('user', __name__, url_prefix='/api/users')


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    return success_response({
        'user': user.to_dict(include_sensitive=True)
    })


@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    if not request.is_json:
        return error_response("Request must be JSON", 400)
    
    data = request.get_json()
    
    try:
        # Update email if provided
        if 'email' in data:
            email = data['email'].strip() if data['email'] else None
            if email:
                # Check if email is already taken by another user
                existing_user = User.query.filter(
                    User.email == email,
                    User.id != user.id
                ).first()
                if existing_user:
                    return error_response("Email already in use", 400)
                user.email = email
        
        # Update password if provided
        if 'password' in data and data['password']:
            new_password = data['password']
            if len(new_password) < 6:
                return error_response("Password must be at least 6 characters", 400)
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        
        return success_response({
            'user': user.to_dict(include_sensitive=True)
        }, "Profile updated successfully")
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating profile: {str(e)}")
        return error_response("Failed to update profile", 500)


@user_bp.route('/me/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    try:
        # Count total images uploaded
        total_images = Image.query.filter_by(uploaded_by=user.id).count()
        
        # Count total classifications
        total_classifications = db.session.query(func.count(ClassificationResult.id))\
            .join(Image)\
            .filter(Image.uploaded_by == user.id)\
            .scalar() or 0
        
        # Count classifications by waste type
        waste_type_counts = db.session.query(
            ClassificationResult.waste_type_id,
            func.count(ClassificationResult.id).label('count')
        )\
        .join(Image)\
        .filter(Image.uploaded_by == user.id)\
        .group_by(ClassificationResult.waste_type_id)\
        .all()
        
        waste_type_stats = {}
        for waste_type_id, count in waste_type_counts:
            from ..models import WasteType
            waste_type = WasteType.query.get(waste_type_id)
            if waste_type:
                waste_type_stats[waste_type.name] = count
        
        # Count feedbacks
        total_feedbacks = Feedback.query.filter_by(user_id=user.id).count()
        
        # Get average confidence score
        avg_confidence = db.session.query(func.avg(ClassificationResult.confidence_score))\
            .join(Image)\
            .filter(Image.uploaded_by == user.id)\
            .scalar() or 0.0
        
        # Get recent activity (last 7 days)
        from datetime import datetime, timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_classifications = db.session.query(func.count(ClassificationResult.id))\
            .join(Image)\
            .filter(
                Image.uploaded_by == user.id,
                ClassificationResult.classified_at >= seven_days_ago
            )\
            .scalar() or 0
        
        return success_response({
            'stats': {
                'total_images': total_images,
                'total_classifications': total_classifications,
                'total_feedbacks': total_feedbacks,
                'average_confidence': round(float(avg_confidence), 4),
                'recent_classifications_7d': recent_classifications,
                'classifications_by_type': waste_type_stats
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching user stats: {str(e)}")
        return error_response("Failed to fetch statistics", 500)

