from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Role(db.Model):
    """Role model for user roles"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    users = db.relationship('User', backref='role', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active
        }


class WasteType(db.Model):
    """Waste type model"""
    __tablename__ = 'waste_types'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255))
    color_code = db.Column(db.String(10), default='#FFFFFF')
    icon_path = db.Column(db.String(255))
    
    # Relationships
    classifications = db.relationship('ClassificationResult', backref='waste_type', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color_code': self.color_code,
            'icon_path': self.icon_path
        }


class User(db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    email = db.Column(db.String(100), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    images = db.relationship('Image', backref='uploader', lazy=True)
    classifications = db.relationship('ClassificationResult', backref='user', lazy=True, 
                                     secondary='images', primaryjoin='User.id==Image.uploaded_by',
                                     secondaryjoin='Image.id==ClassificationResult.image_id',
                                     viewonly=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        if include_sensitive:
            data['role_id'] = self.role_id
            if self.role:
                data['role'] = self.role.to_dict()
        return data


class Image(db.Model):
    """Image model for uploaded images"""
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(50))
    is_temporary = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    classification_results = db.relationship('ClassificationResult', backref='image', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_path': self.image_path,
            'original_name': self.original_name,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'is_temporary': self.is_temporary,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'uploaded_by': self.uploaded_by
        }


class ClassificationResult(db.Model):
    """Classification result model"""
    __tablename__ = 'classification_results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id', ondelete='CASCADE'), nullable=False)
    waste_type_id = db.Column(db.Integer, db.ForeignKey('waste_types.id'), nullable=False)
    classified_at = db.Column(db.DateTime, default=datetime.utcnow)
    confidence_score = db.Column(db.Float)
    model_version = db.Column(db.String(50), default='v1.0')
    processing_time_ms = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='success')
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='classification', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_image=False, include_waste_type=True):
        data = {
            'id': self.id,
            'image_id': self.image_id,
            'waste_type_id': self.waste_type_id,
            'classified_at': self.classified_at.isoformat() if self.classified_at else None,
            'confidence_score': self.confidence_score,
            'model_version': self.model_version,
            'processing_time_ms': self.processing_time_ms,
            'status': self.status
        }
        if include_image and self.image:
            data['image'] = self.image.to_dict()
        if include_waste_type and self.waste_type:
            data['waste_type'] = self.waste_type.to_dict()
        return data


class Feedback(db.Model):
    """Feedback model for user feedback on classifications"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification_id = db.Column(db.Integer, db.ForeignKey('classification_results.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    feedback_text = db.Column(db.String(255))
    feedback_type = db.Column(db.String(20), default='neutral')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self, include_classification=False):
        data = {
            'id': self.id,
            'classification_id': self.classification_id,
            'user_id': self.user_id,
            'feedback_text': self.feedback_text,
            'feedback_type': self.feedback_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_classification and self.classification:
            data['classification'] = self.classification.to_dict(include_waste_type=True)
        return data

