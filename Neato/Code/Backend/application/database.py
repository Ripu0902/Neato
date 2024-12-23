from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash
from sqlalchemy import CheckConstraint
from datetime import datetime, timezone
import enum



db = SQLAlchemy()

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class ServiceStatus(enum.Enum):
    REQUESTED = 'REQUESTED'
    ASSIGNED = 'ASSIGNED'
    IN_PROGRESS = "IN_PROGRESS"
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Roles(db.Model):
    __tablename__="roles"
    role_id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String,nullable=False)

    def __int__(self,role_id,role_name):
        self.role_id = role_id
        self.role_name =role_name


class User(db.Model):
    __tablename__="user"
    user_id = db.Column(db.String,primary_key=True,default=lambda: str(uuid.uuid4()))
    username= db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.role_id'),nullable=False)
    is_blocked = db.Column(db.Boolean,default=False)

    professional = db.relationship('Professional', back_populates='user', cascade="all, delete", uselist=False)
    customer = db.relationship('Customer', back_populates='user', cascade="all, delete", uselist=False)

    def __init__(self,username,password,role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
        self.is_blocked = False
    
    def to_dict(self):
        return {
            'user_id' : self.user_id,
            'username' : self.username,
            'is_blocked' : self.is_blocked,
            'role' : self.role
        }

class Customer(db.Model):
    __tablename__="customer"
    customer_id = db.Column(db.String,db.ForeignKey('user.user_id'),primary_key=True)
    fullname= db.Column(db.String,nullable=False)
    contact = db.Column(db.String(10), nullable=False)  # Ensure it's a 10-character string
    email = db.Column(db.String(120), unique=True, nullable=False)
    primary_address = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String)

    user = db.relationship('User', back_populates='customer')

    __table_args__ = (
        CheckConstraint('LENGTH(contact) = 10', name='check_contact_length'),
    )

    def to_dict(self):
        return {
            'customer_id' : self.customer_id,
            'fullname' : self.fullname,
            'contact' : self.contact,
            'email' : self.email,
            'address' : self.primary_address,
            'profile_image' :self.profile_image
        }

class Professional(db.Model):
    __tablename__="professional"
    professional_id= db.Column(db.String,db.ForeignKey('user.user_id'),primary_key=True)
    fullname = db.Column(db.String,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(10), nullable=False)  # Ensure it's a 10-character string
    service_type = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable = False)
    service_pincode = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    description = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    profile_image = db.Column(db.String)
    document_path = db.Column(db.String(255))
    isActive = db.Column(db.Integer,nullable=False)
    kudos = db.Column(db.Integer,default=0)
    
    user = db.relationship('User', back_populates='professional')

    __table_args__ = (
        CheckConstraint('experience >= 0', name='check_experience_positive'),
        CheckConstraint('isActive IN (0, 1,2)', name='check_isActive_values'),
    )

    def update_last_seen(self):
        try:
            self.last_seen = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {'error' : f'An error occured while changing last seen : {e}'}
    
    def to_dict(self):
        return {
            'professional_id': self.professional_id,
            'fullname': self.fullname,
            'contact' : self.contact,
            'email' : self.email,
            'service_type' : self.service_type,
            'service_pincode' : self.service_pincode,
            'experience' : self.experience,
            'description' : self.description,
            'document_path' : self.document_path,
            'profile_image': self.profile_image,
            'date_created' : self.date_created.isoformat(),
            'isActive' : self.isActive,
            'kudos' : self.kudos
        }


class Services(db.Model):
    __tablename__="services"
    service_id = db.Column(db.Integer,primary_key=True)
    service_name = db.Column(db.String,nullable=False)
    description = db.Column(db.String(200))
    price= db.Column(db.Float,nullable=False)
    time_required = db.Column(db.Integer,nullable=False)   # in minutes
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    category = db.Column(db.String, nullable=False)

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )

    def to_dict(self):
        return {
            'service_id': self.service_id,
            'service_name': self.service_name,
            'price': self.price,
            'time_required': self.time_required,
            'description': self.description,
            'category' : self.category,
            'date_created' :f'{self.date_created}'[:10]
        }


class Service_request(db.Model):
    __tablename__="service_request"
    service_request_id = db.Column(db.Integer,primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'),nullable=False)
    customer_id = db.Column(db.String,db.ForeignKey('customer.customer_id'),nullable=False)
    professional_id = db.Column(db.String,db.ForeignKey('professional.professional_id'))
    date_of_request = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(db.Enum(ServiceStatus), nullable=False, default=ServiceStatus.REQUESTED)
    remarks = db.Column(db.String(100))
    ratings = db.Column(db.Integer, default=0)

    def completed(self):
        try:
            self.date_of_completion = datetime.now(timezone.utc)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error' : f'An error occured while changing completion date : {e}'}

    def to_dict(self):
        def serialize_datetime(dt):
            if isinstance(dt, datetime):
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            return dt
        return {
            "service_request_id": self.service_request_id,
            "service_id": self.service_id,
            "customer_id": self.customer_id,
            "professional_id": self.professional_id,
            "date_of_request": serialize_datetime(self.date_of_request),
            "date_of_completion": serialize_datetime(self.date_of_completion),
            "service_status": self.service_status.value if self.service_status else None,
            "remarks": self.remarks,
            "ratings" : self.ratings
        }


