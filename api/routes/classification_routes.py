from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from ..models import db, Image, ClassificationResult, WasteType
from ..utils import (
    error_response, success_response, get_current_user,
    save_uploaded_file, get_file_size, get_mime_type, paginate_query
)
from ..services.classification_service import classification_service

classification_bp = Blueprint('classification', __name__, url_prefix='/api')


@classification_bp.route('/classify', methods=['POST'])
@jwt_required()
def classify_waste():
    """Upload image and classify waste type"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    # Check if file is present
    if 'image' not in request.files:
        return error_response("No image file provided", 400)
    
    file = request.files['image']
    if file.filename == '':
        return error_response("No file selected", 400)
    
    # Save uploaded file
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    file_path, original_name = save_uploaded_file(file, upload_folder)
    
    if not file_path:
        return error_response("Failed to save file or invalid file type", 400)
    
    try:
        # Get file info
        file_size = get_file_size(file_path)
        mime_type = get_mime_type(original_name)
        
        # Create image record
        image = Image(
            image_path=file_path,
            original_name=original_name,
            file_size=file_size,
            mime_type=mime_type,
            is_temporary=False,
            uploaded_by=user.id
        )
        db.session.add(image)
        db.session.flush()  # Get image.id
        
        # Classify image
        prediction_result = classification_service.predict(file_path)
        
        # Get or create waste type
        waste_type_name = prediction_result['waste_type']
        waste_type = WasteType.query.filter_by(name=waste_type_name).first()
        
        if not waste_type:
            # Create waste type if it doesn't exist
            waste_type = WasteType(
                name=waste_type_name,
                description=f"Waste type: {waste_type_name}"
            )
            db.session.add(waste_type)
            db.session.flush()
        
        # Create classification result
        classification = ClassificationResult(
            image_id=image.id,
            waste_type_id=waste_type.id,
            confidence_score=prediction_result['confidence_score'],
            model_version=prediction_result.get('model_version', 'v1.0'),
            processing_time_ms=prediction_result.get('processing_time_ms', 0),
            status='success'
        )
        db.session.add(classification)
        db.session.commit()
        
        # Return result
        return success_response({
            'classification': classification.to_dict(include_waste_type=True, include_image=True),
            'prediction_details': {
                'all_predictions': prediction_result.get('all_predictions', {}),
                'processing_time_ms': prediction_result.get('processing_time_ms', 0)
            }
        }, "Classification completed successfully")
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Classification error: {str(e)}")
        return error_response(f"Classification failed: {str(e)}", 500)


@classification_bp.route('/classifications', methods=['GET'])
@jwt_required()
def get_classifications():
    """Get user's classification history"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query classifications through images uploaded by user
        query = db.session.query(ClassificationResult)\
            .join(Image)\
            .filter(Image.uploaded_by == user.id)\
            .order_by(desc(ClassificationResult.classified_at))
        
        # Paginate
        pagination = paginate_query(query, page, per_page)
        
        # Serialize results
        classifications = [
            item.to_dict(include_waste_type=True, include_image=True)
            for item in pagination['items']
        ]
        
        return success_response({
            'classifications': classifications,
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
        current_app.logger.error(f"Error fetching classifications: {str(e)}")
        return error_response("Failed to fetch classifications", 500)


@classification_bp.route('/classifications/<int:classification_id>', methods=['GET'])
@jwt_required()
def get_classification_detail(classification_id):
    """Get specific classification details"""
    user = get_current_user()
    if not user:
        return error_response("User not found", 404)
    
    try:
        # Get classification and verify ownership
        classification = db.session.query(ClassificationResult)\
            .join(Image)\
            .filter(
                ClassificationResult.id == classification_id,
                Image.uploaded_by == user.id
            )\
            .first()
        
        if not classification:
            return error_response("Classification not found", 404)
        
        return success_response({
            'classification': classification.to_dict(
                include_waste_type=True,
                include_image=True
            )
        })
        
    except Exception as e:
        current_app.logger.error(f"Error fetching classification: {str(e)}")
        return error_response("Failed to fetch classification", 500)

