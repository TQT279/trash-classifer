from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from ..models import db, Feedback, ClassificationResult, Image
from ..utils import (
    error_response, success_response, get_current_user,
    validate_request_json, paginate_query
)

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api')


@feedback_bp.route('/feedbacks', methods=['POST'])
@jwt_required()
def submit_feedback():
    """Submit feedback on a classification"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    is_valid, missing = validate_request_json(['classification_id'])
    if not is_valid:
        return error_response(f"Missing required fields: {', '.join(missing)}", 400)
    
    data = request.get_json()
    classification_id = data.get('classification_id')
    feedback_text = data.get('feedback_text', '').strip()
    feedback_type = data.get('feedback_type', 'neutral').strip().lower()
    
    # Validate feedback type
    valid_types = ['positive', 'negative', 'neutral']
    if feedback_type not in valid_types:
        return error_response(f"Invalid feedback_type. Must be one of: {', '.join(valid_types)}", 400)
    
    try:
        # Verify classification exists and belongs to user
        classification = db.session.query(ClassificationResult)\
            .join(Image)\
            .filter(
                ClassificationResult.id == classification_id,
                Image.uploaded_by == user.id
            )\
            .first()
        
        if not classification:
            return error_response("Classification not found or access denied", 404)
        
        # Check if feedback already exists for this classification
        existing_feedback = Feedback.query.filter_by(
            classification_id=classification_id,
            user_id=user.id
        ).first()
        
        if existing_feedback:
            # Update existing feedback
            existing_feedback.feedback_text = feedback_text
            existing_feedback.feedback_type = feedback_type
            db.session.commit()
            
            return success_response({
                'feedback': existing_feedback.to_dict(include_classification=True)
            }, "Feedback updated successfully")
        else:
            # Create new feedback
            feedback = Feedback(
                classification_id=classification_id,
                user_id=user.id,
                feedback_text=feedback_text,
                feedback_type=feedback_type
            )
            db.session.add(feedback)
            db.session.commit()
            
            return success_response({
                'feedback': feedback.to_dict(include_classification=True)
            }, "Feedback submitted successfully", 201)
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting feedback: {str(e)}")
        return error_response("Failed to submit feedback", 500)


@feedback_bp.route('/feedbacks', methods=['GET'])
@jwt_required()
def get_feedbacks():
    """Get user's feedback history"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        feedback_type = request.args.get('type', None)
        
        # Build query
        query = Feedback.query.filter_by(user_id=user.id)
        
        if feedback_type:
            query = query.filter_by(feedback_type=feedback_type)
        
        query = query.order_by(desc(Feedback.created_at))
        
        # Paginate
        pagination = paginate_query(query, page, per_page)
        
        # Serialize results
        feedbacks = [
            item.to_dict(include_classification=True)
            for item in pagination['items']
        ]
        
        return success_response({
            'feedbacks': feedbacks,
            'pagination': {
                'total': pagination['total'],
                'page': pagination['page'],
                'per_page': pagination['per_page'],
                'pages': pagination['pages'],
                'has_next': pagination['has_next'],
                'has_prev': pagination['has_prev']
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching feedbacks: {str(e)}")
        return error_response("Failed to fetch feedbacks", 500)


@feedback_bp.route('/feedbacks/<int:feedback_id>', methods=['DELETE'])
@jwt_required()
def delete_feedback(feedback_id):
    """Delete a feedback"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    try:
        feedback = Feedback.query.filter_by(
            id=feedback_id,
            user_id=user.id
        ).first()
        
        if not feedback:
            return error_response("Feedback not found", 404)
        
        db.session.delete(feedback)
        db.session.commit()
        
        return success_response(None, "Feedback deleted successfully")
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting feedback: {str(e)}")
        return error_response("Failed to delete feedback", 500)

