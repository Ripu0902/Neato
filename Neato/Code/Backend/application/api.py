from flask_restful import Resource

from flask import request
from flask_jwt_extended import create_access_token, jwt_required,get_jwt_identity
from werkzeug.security import check_password_hash,generate_password_hash
from application.database import *
from sqlalchemy.exc import IntegrityError
import os
from application.config import LocalDevelopementConfig
# from application.tasks import generate_service_export
# from celery import shared_task
# from app import celery
from werkzeug.utils import secure_filename
from sqlalchemy.orm import joinedload
from .utils import CacheManager
from nltk.sentiment import SentimentIntensityAnalyzer
from sqlalchemy import and_
import re

def analyze_sentiment(text, rating=None):
    """
    Analyze sentiment of review text using NLTK's VADER sentiment analyzer
    and combine it with numerical rating if provided.
    
    Args:
        text (str): Review text
        rating (float, optional): Numerical rating (1-5 scale)
    
    Returns:
        dict: Sentiment analysis results including scores and category
    """
    # Clean the text
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    
    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Get VADER sentiment scores
    sentiment_scores = sia.polarity_scores(text)
    
    # Calculate weighted score (0-100 scale)
    text_score = ((sentiment_scores['compound'] + 1) / 2) * 100
    
    # If rating is provided, combine it with text sentiment
    if rating is not None:
        # Convert rating to 0-100 scale
        rating_score = (rating / 5) * 100
        # Combine scores (60% weight to text, 40% to rating)
        final_score = (text_score * 0.6) + (rating_score * 0.4)
    else:
        final_score = text_score
    
    return round(final_score, 0)


serviceMapping = {1:"General Home Cleaning",2:"Deep Cleaning",3:"Kitchen Cleaning",4:"Bathroom Cleaning",5:"Sofa and Carpet Cleaning",6:"Window and Glass Cleaning",7:"Electrical Repairs",8:"Fan Installation and Repairs",9:"Light and Socket Fitting",10:"Wiring and Electrical Panel Work",11:"Appliance Installation",12:"Leak Repairs",13:"Pipe Fitting and Replacement",14:"Faucet and Sink Repair",15:"Water Tank Cleaning",16:"Bathroom Fittings Installation",17:"AC Installation and Servicing",18:"Refrigerator Repair",19:"Washing Machine Repair",20:"Microwave Oven Repair",21:"Water Purifier Installation and Servicing",22:"Furniture Repair",23:"Custom Furniture Building",24:"Door and Window Fitting",25:"Lock and Handle Repairs",26:"Modular Kitchen Installations",27:"Wall Painting",28:"Textured Wall Designs",29:"Polishing and Wood Painting",30:"Waterproofing Solutions",31:"Termite Control",32:"Cockroach Control",33:"Mosquito Control",34:"Bed Bug Control",35:"Rodent Control",36:"Flooring and Tiling",37:"Bathroom Remodeling",38:"Waterproofing",39:"Masonry Work",40:"Lawn Mowing and Maintenance",41:"Plant Installation",42:"Garden Designing",43:"Tree Trimming and Removal",44:"CCTV Installation",45:"Home Automation",46:"Doorbell and Intercom Installation",47:"Handyman Services",48:"Pack and Move Services",49:"Home Sanitization Services",50:"Curtain and Blind Installation"}


def validate_password(password):
   if not 8 <= len(password) <= 15:
       return False, "Password must be between 8 and 15 characters"
       
   if not any(c.islower() for c in password):
       return False, "Password must contain lowercase letter"
       
   if not any(c.isupper() for c in password):
       return False, "Password must contain uppercase letter"
       
   if not any(c.isdigit() for c in password):
       return False, "Password must contain a number"
       
   if not any(c in "!@#$%^&*" for c in password):
       return False, "Password must contain special character (!@#$%^&*)"
       
   return True, "Password valid"

def valid_user(user):
    if(user['role'] == 0): return True ,'admin'
    if(user['role'] == 1): return True, 'customer'
    if(user['role'] == 2): return True, 'professional'
    return False, 'Invalid User'

def is_valid_uuid(uuid_str):
    # Regex for validating UUID format
    uuid_regex = re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
    return bool(uuid_regex.match(uuid_str))


class CustomerSignupApi(Resource):
    def post(self):
        try:
            # Required fields for validation
            required_fields = ['username', 'password', 'firstName','lastName', 'contact', 'email', 'houseNo', 'locality', 'city', 'state', 'pincode' ]

            # Check if all required fields are in request.form
            missing_fields = [field for field in required_fields if not request.form.get(field)]

            if missing_fields:
                return {
                    "message": "Validation Error",
                    "error": f"Missing fields: {', '.join(missing_fields)}"
                }, 400
            
            is_valid, message = validate_password(request.form.get('password'))
            if not is_valid:
                return {"error": message}, 400


             # Extracting data after validation
            username = request.form.get('username')
            password = request.form.get('password')
            fullname = request.form.get('firstName') +" "+ request.form.get('lastName')
            contact = request.form.get('contact')
            email = request.form.get('email')
            primary_address = request.form.get('houseNo')+" "+request.form.get('locality')+" "+request.form.get('city')+" "+request.form.get('state')+" "+request.form.get('pincode')

            print(username,password,fullname,contact,email,primary_address)

            # print(User.query.filter_by(username=username).first())
            # Check if username or email already exists
            if User.query.filter_by(username=username).first():
                return{'message': 'User already exist'}, 400
            
            if Customer.query.filter_by(email=email).first():
                return {'message': 'Email already exists'}, 409

            # Validate profile image
            if 'profile_image' in request.files:
                try:    
                    profile_image = request.files['profile_image']
                    image_filename = secure_filename(f"{username}_profile.{profile_image.filename.split('.')[-1]}")
                    image_file_path = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, image_filename)
                    profile_image.save(image_file_path)
                except Exception as e:
                    return {
                        "message": f"Error saving profile image: {e}"
                    }, 400
            else:
                image_file_path = None

            # Create User and Customer objects
            new_user = User(username=username, password=password, role=1)
            db.session.add(new_user)
            db.session.commit()

            new_customer = Customer(
                customer_id=new_user.user_id,
                fullname=fullname,
                contact=contact,
                email=email,
                primary_address=primary_address,
                profile_image=image_file_path
            )
            db.session.add(new_customer)
            db.session.commit()

            return {'message': 'User registered successfully'}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred: {str(e)}'}, 500

class LoginApi(Resource):
    def post(self):
        
        try:
            # Get form data
            user_name = request.form.get('username')
            pass_word = request.form.get('password')
            print(user_name)
            # Check if required fields are provided
            if not user_name or not pass_word:
                return {
                    'message': 'Missing required fields (username, password)'
                }, 400

            # Query the database for the user
            user = User.query.filter_by(username=user_name).first()
            print(user)
            if not user:
                return {
                    'message': 'Invalid username or password'
                }, 401
            
            # Check password
            if not check_password_hash(user.password, pass_word):
                return {
                    'message': 'Invalid username or password'
                }, 401

            if user.role==2:
                try:
                    prof = Professional.query.filter_by(professional_id=user.user_id).first()
                    prof.update_last_seen()
                    db.session.commit()
                    print(f'Date updated')
                except Exception as e:
                    db.session.rollback()
                    print(f'Not updated')
                    

            # Create access token
            access_token = create_access_token(identity={
                'userid': user.user_id,
                'role': user.role
            })
            

            return  {
                'access_token': access_token,
                'role' : user.role
            }, 200

        except Exception as e:
            return {
                'message': f'An error occurred: {str(e)}'
            }, 500

class UserDetails(Resource):
    @jwt_required()
    @CacheManager.cached(timeout=300, key_prefix='user')
    def get(self):
        current_user = get_jwt_identity()

        userflag, usertype = valid_user(current_user)
        print(userflag,usertype)

        if(userflag and (usertype=='admin')): 
            admindata = User.query.get(current_user['userid'])

            return {'admindata': admindata.to_dict() }, 200
        if(not userflag): return {'message': usertype}, 403

        userdata = User.query.filter_by(user_id=current_user['userid']).first()
        if(not userdata):
            return{
                'message' : 'User Not found'
            }, 404

        if current_user['role'] == 1:
            try:
                customerdata = Customer.query.filter_by(customer_id=current_user['userid']).first()
                return{
                    'userdata' : userdata.to_dict(),
                    'customerdata' : customerdata.to_dict()
                }, 200
            except Exception as e :
                return {
                    'message': 'Error getting customer-specific data'
                }, 400
        elif current_user['role'] == 2:
            try:
                profdata = Professional.query.filter_by(professional_id=current_user['userid']).first()
                return{
                    'userdata' : userdata.to_dict(),
                    'professionaldata' : profdata.to_dict()
                }
            except Exception as e :
                return {
                    'message': 'Error getting data professional specific data.'
                }, 400

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()

        userflag, usertype = valid_user(current_user)

        if(userflag and (usertype=='admin')): return {'message': "Admin can't access this API."}, 403
        if(not userflag): return {'message': usertype}, 403

        userdata = User.query.filter_by(user_id=current_user['userid']).first()
        print(f'User data : {userdata}')

        if(not userdata): return {'message':'User not found'}, 404

        print(request.form.get('address'))
            
        try:
            if(userflag and usertype=='customer'):
                customerdata = Customer.query.filter_by(customer_id=current_user['userid']).first()

                if  request.form.get('fullname'):
                    customerdata.fullname = request.form.get('fullname')
                if request.form.get('contact'):
                    customerdata.contact = request.form.get('contact')
                if request.form.get('email'):
                    customerdata.email = request.form.get('email')
                if request.form.get('address'):
                    customerdata.primary_address = request.form.get('address')
                if (request.form.get('password')):
                    setattr(userdata,'password',generate_password_hash(request.form.get('password')))
    
                if 'profile_image' in request.files:
                    profile_image = request.files['profile_image']

                    # Secure the filename and construct the file path
                    username = userdata.username  # Assuming username is the same as customer_id
                    extension = profile_image.filename.split('.')[-1]
                    image_filename = secure_filename(f"{username}_profile.{extension}")
                    image_file_path = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, image_filename)

                    # Save the image file
                    profile_image.save(image_file_path)

                    # Update the database
                    customerdata.profile_image = image_file_path
                db.session.commit()
                CacheManager.clear_user_caches(current_user['userid'])
                return {'message' : "Details updated Successfully"}, 200
            elif(userflag and usertype=='professional'):
                print(current_user['userid'])
                profdata = Professional.query.filter_by(professional_id=current_user['userid']).first()
                print(request.form)

                if request.form.get('fullname'):
                    profdata.fullname = request.form.get('fullname')
                if  request.form.get('contact'):
                    profdata.contact = request.form.get('contact')
                if  request.form.get('email'):
                    profdata.email = request.form.get('email')
                if  request.form.get('experience'):
                    profdata.experience = request.form.get('experience')
                if  request.form.get('description'):
                    profdata.description = request.form.get('description')
                if request.form.get('service_pincode'):
                    profdata.service_pincode = request.form.get('service_type')
                if (request.form.get('password')):
                    setattr(userdata,'password',generate_password_hash(request.form.get('password')))
                if 'profile_image' in request.files:
                    profile_image = request.files['profile_image']
                    
                    
                    # Secure the filename and construct the file path
                    username = userdata.username  # Assuming username is the same as customer_id
                    extension = profile_image.filename.split('.')[-1]
                    image_filename = secure_filename(f"{username}_profile.{extension}")
                    image_file_path = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, image_filename)

                    # Save the image file
                    profile_image.save(image_file_path)

                    # Update the database
                    profdata.profile_image = image_file_path

                if 'portfolio' in request.files:
                    portfolio_document = request.files['portfolio']
                    print(portfolio_document)

                    # Secure the filename and construct the file path
                    username = userdata.username  # Assuming username is the same as professional_id
                    extension = portfolio_document.filename.split('.')[-1]
                    portfolio_filename = secure_filename(f"{username}_portfolio.{extension}")
                    portfolio_file_path = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, portfolio_filename)

                    # Save the document file
                    portfolio_document.save(portfolio_file_path)

                    # Update the database
                    profdata.document_path = portfolio_file_path

                    # Professional have to again verified so change the isActive
                    profdata.isActive = 0

                print(profdata)
                db.session.commit()
                CacheManager.clear_user_caches(current_user['userid'])
                return {'message' : "Details updated Successfully"}, 200
                    
        except Exception as e: return {"message": f"An error occurred: {str(e)}"}, 500

    @jwt_required
    def delete():
        current_user = get_jwt_identity()
        userflag, usertype = valid_user(current_user)
        try:
            if(userflag and usertype=='customer'):
                userdata = User.query.filter_by(username=current_user['userid']).first()
                if userdata:
                    customerdata = Customer.query.filter_by(customer_id=current_user['userid']).first()
                    if customerdata:
                        if customerdata.profile_image and os.path.exists(customerdata.profile_image):
                            os.remove(customerdata.profile_image)
                        db.session.delete(customerdata)
                        db.session.delete(userdata)
                    else:
                        return {'message': "Customer doesn't exist"}, 404
                else:
                    return {'message' : "User doesn't exist"}, 404
            
                return {'message' : "Account deleted successfully" }, 200        
            elif(userflag and usertype=='professional'):
                userdata = User.query.filter_by(username=current_user['userid']).first()
                if userdata:
                    profdata = Professional.query.filter_by(professional_id=current_user['userid']).first()
                    if profdata:
                        if profdata.profile_image and os.path.exists(profdata.profile_image):
                            os.remove(profdata.profile_image)
                        if profdata.document_path and os.path.exists(profdata.document_path):
                            os.remove(profdata.document_path)
                        db.session.delete(profdata)
                        db.session.delete(userdata)
                    else:
                        return {'message': "Professional doesn't exist"}, 404
                else:
                    return {'message' : "User doesn't exist"}, 404
                return {'message' : "Account deleted successfully" }, 200
        except Exception as e: return {"message": f"An error occurred: {str(e)}"}, 500

class AdminApi(Resource):
    @jwt_required()
    @CacheManager.cached(timeout=180, key_prefix='admin')  # 3-minute cache
    def get(self,user_id=None):
        current_user = get_jwt_identity()
        userflag, usertype = valid_user(current_user)
        if userflag :
            if (usertype!='admin'): 
                return { 'message' , 'You are not authorized'}, 403
            else:
                if user_id:
                    try:
                        if not is_valid_uuid(user_id):
                            return {"message": "Invalid user_id format"}, 400
                        user = (
                            User.query
                            .options(joinedload(User.customer), joinedload(User.professional))
                            .filter_by(user_id=user_id)
                            .first()
                        )

                        # If the user does not exist
                        if not user:
                            return ({"message": "User not found"}), 404

                        # Determine role and fetch corresponding data
                        if user.role == 1:  # Role = 1, Customer
                            if user.customer:
                                user_data = {**user.to_dict(), **user.customer.to_dict()}
                            else:
                                return ({"message": "Customer data not found for this user"}), 404
                        elif user.role == 2:  # Role = 2, Professional
                            if user.professional:
                                user_data = {**user.to_dict(), **user.professional.to_dict()}
                            else:
                                return ({"message": "Professional data not found for this user"}), 404
                        else:
                            return ({"message": "Invalid role or no associated data"}), 400

                        # Return the combined data as JSON
                        return { 'user':user_data}, 200

                    except Exception as e:
                        return {"error": str(e)}, 500
                else:
                    try:
                        # Fetch customer data (role = 1)
                        customerdata = (
                            User.query
                            .options(joinedload(User.customer))
                            .filter(User.role == 1)
                            .all()
                        )
                        
                        # If no customer data, return an empty list
                        result_customer = [
                            {**user.to_dict(), **(user.customer.to_dict() if user.customer else {})}
                            for user in customerdata
                        ] if customerdata else []

                        # Fetch professional data (role = 2)
                        professionaldata = (
                            User.query
                            .options(joinedload(User.professional))
                            .filter(User.role == 2)
                            .all()
                        )
                        
                        # If no professional data, return an empty list
                        result_professional = [
                            {**user.to_dict(), **(user.professional.to_dict() if user.professional else {})}
                            for user in professionaldata
                        ] if professionaldata else []

                        # Prepare the final response
                        return {
                            "customerdata": result_customer,
                            "professionaldata": result_professional,
                            "service-mapping" : serviceMapping
                        }, 200

                    except Exception as e:
                        return {"error": str(e)}, 500
        else: return {'message' : f'You are an {usertype}.'}, 403

class ToggleBlockApi(Resource):
    @jwt_required()
    def patch(Resource, user_id):
        current_user = get_jwt_identity()
        if user_id:
            userflag, usertype = valid_user(current_user)
            if userflag:
                if (usertype!='admin'): return {'message' : 'Not Authorized'}, 403
                else:
                    try:
                        userdata = User.query.filter_by(user_id=user_id).first()
                        userdata.is_blocked = not userdata.is_blocked
                        db.session.commit()
                        # Clear user caches
                        CacheManager.clear_user_caches(user_id)
                        return {'message': 'Status updated successfully'}, 200
                    except Exception as e:
                        return {'message' : f'An error occured: {e}'}, 500

            else: return {'message' : f'You are an {usertype}'}, 403  
        else: 
            return {'message': 'Provide valid user id'}, 404 

class VerifyProfessionalApi(Resource):
    @jwt_required()
    def patch(self, professional_id):
        current_user = get_jwt_identity()
        print(professional_id)
        if professional_id:
            userflag, usertype = valid_user(current_user)
            if userflag:
                if usertype != 'admin':
                    return {'message': 'Not Authorized'}, 403
                else:
                    try:
                        # Parse form data for the action
                        action = request.form.get('action')  # 'accept' or 'reject'

                        if not action or action not in ['accept', 'reject']:
                            return {'message': 'Invalid or missing action. Use "accept" or "reject".'}, 400
                        
                        profdata = Professional.query.get(professional_id)
                        if not profdata:
                            return {'message': 'Professional not found.'}, 404
                        
                        if action == 'accept':
                            profdata.isActive = 1
                            message = 'Verification accepted successfully.'
                        elif action == 'reject':
                            profdata.isActive = 2
                            message = 'Verification rejected successfully.'

                        db.session.commit()

                        CacheManager.clear_user_caches(professional_id)
                        CacheManager.clear_service_caches()  # Since this affects service search
                        return {'message': message}, 200
                    except Exception as e:
                        return {'message': f'An error occurred: {e}'}, 500
            else:
                return {'message': f'You are an {usertype}'}, 403
        else:
            return {'message': 'Provide valid professional ID'}, 404



class ProfessionalSignupApi(Resource):
    def post(self):
        try:
            # Required fields validation
            print(request.form)
            required_fields = ['username', 'password', 'firstName', 'lastName', 'contact', 'email', 'service_type', 'experience', 'service_pincode','experience', 'description', ]
            required_files = ['profile_image', 'portfolio']

            # Check if all required fields are in request.form
            missing_fields = [field for field in required_fields if not request.form.get(field)]
            if missing_fields:
                return {
                    "message": f"Validation Error 1 {', '.join(missing_fields)}",
                    "error": f"Missing fields: {', '.join(missing_fields)}"
                }, 400

            # Check if all required files are in request.files
            missing_files = [field for field in required_files if not request.files.get(field)]
            if missing_files:
                return {
                    "message": "Validation Error 2",
                    "error": f"Missing files: {', '.join(missing_files)}"
                }, 400

            # Extract data from form
            username = request.form.get('username')
            password = request.form.get('password')
            fullname = request.form.get('firstName') +" "+ request.form.get('lastName')
            contact = request.form.get('contact')
            email = request.form.get('email')
            
            service_type = request.form.get('service_type')
            

            experience = int(request.form.get('experience'))
            service_pincode = int(request.form.get('service_pincode'))
            description = request.form.get('description')

            is_valid, message = validate_password(request.form.get('password'))
            if not is_valid:
                return {"error": message}, 400

            # Check if username or email already exists
            if User.query.filter_by(username=username).first():
                return {'message': 'Username already exists'}, 409
            if Professional.query.filter_by(email=email).first():
                return {'message': 'Email already exists'}, 409

            # Handle profile image
            profile_image = request.files['profile_image']
            image_filename = secure_filename(f"{username}_profile.{profile_image.filename.split('.')[-1]}")
            print(image_filename)
            image_file_path = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, image_filename)
            profile_image.save(image_file_path)
            print(image_file_path)

            # Handle portfolio document
            portfolio_document = request.files['portfolio']
            portfolio_filename = f"{username}_portfolio.{portfolio_document.filename.split('.')[-1]}"
            portfolio_file_path = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, portfolio_filename)
            portfolio_document.save(portfolio_file_path)

            # Create User and Professional objects
            new_user = User(username=username, password=password, role=2)  # Role 2 for Professional
            db.session.add(new_user)
            db.session.commit()

            new_professional = Professional(
                professional_id=new_user.user_id,
                fullname=fullname,
                contact=contact,
                email=email,
                description=description,
                service_type=service_type,
                service_pincode=service_pincode,
                experience=experience,
                profile_image=image_file_path,
                document_path=portfolio_file_path,
                isActive=False  # Initially inactive for admin approval
            )
            db.session.add(new_professional)
            db.session.commit()

            return {'message': 'Professional request sent successfully'}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred: {str(e)}'}, 500

class ServiceApi(Resource):
    @CacheManager.cached(timeout=300, key_prefix='service')
    def is_admin(self):
        # Get the role from the JWT token
        current_user = get_jwt_identity()
        if current_user.get('role') != 0:  # Check if role is not admin (0)
            return False
        return True

    def get(self, service_id=None):

        if service_id is None:
            # Fetch and return all services
            services = Services.query.all()
            services_list = [service.to_dict() for service in services]
            return { 'services' : services_list }, 200
        else:
            # Fetch and return a specific service by ID
            service = Services.query.get(int(service_id))
            if not service:
                return {'message': 'Service not found'}, 404
            return service.to_dict()
    
    @jwt_required()
    def post(self):
        if not self.is_admin():
            return {'message': 'Access denied. Admins only.'}, 403

        service_name = request.form.get('service_name')
        description = request.form.get('description')
        price = request.form.get('price')
        time_required = request.form.get('time_required')
        category = request.form.get('category')

        if not all([service_name, description, price, time_required, category]):
            return {'message': 'Missing required fields'}, 400

        try:
            service = Services(
                service_name=service_name,
                description=description,
                price=price,
                time_required=time_required,
                category=category
            )
            db.session.add(service)
            db.session.commit()
            CacheManager.clear_service_caches()
            return {'message': 'Service created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred: {str(e)}'}, 500
    
    @jwt_required()
    def put(self, service_id):

        if not self.is_admin: return {'message' : 'Not authorized'}, 404

        service = Services.query.filter_by(service_id=service_id).first()

        if not service : return {'mesaage' : 'Service Not Found'}, 400
        try:
            # Get form data using request.form
            form_data = request.form
            
            # Update service attributes if they exist in form data
            if form_data.get('service_name'): 
                service.service_name = form_data.get('service_name')
            
            if form_data.get('description'): 
                service.description = form_data.get('description')
            
            if form_data.get('price'): 
                service.price = float(form_data.get('price'))  # Convert to float for price
            
            if form_data.get('time_required'): 
                service.time_required = form_data.get('time_required')
            
            if form_data.get('category'): 
                service.category = form_data.get('category')
            
            db.session.commit()
            return {'message': 'Service updated successfully!'}, 200

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of error
            return {'error': f'An error occurred: {str(e)}'}, 500

    @jwt_required()
    def delete(self, service_id):
        if not self.is_admin():
            return {'message': 'Access denied. Admins only.'}, 403

        print(service_id)
        service_id = int(service_id)
        service = Services.query.get(service_id)

        if not service:
            return {'message': 'Service not found'}, 404
        try:
            db.session.delete(service)
            db.session.commit()
            return {'message': 'Service deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500
        


class ServiceSearchAPI(Resource):
    @jwt_required()
    @CacheManager.cached(timeout=300, key_prefix='search')  
    def get(self):
        try:
            search_query = request.args.get('query', '')
            print(search_query)
            # Get current user's customer_id from token
            current_user = get_jwt_identity()
            
            # Get customer details to extract pincode
            customer = Customer.query.filter_by(customer_id=current_user['userid']).first()
            if not customer:
                return {'message': 'Customer not found'}, 404
                
            # Extract pincode from primary_address (assuming last 6 digits)
            address_parts = customer.primary_address.split()
            customer_pincode = int(address_parts[-1])  # Convert to int since service_pincode is integer
            print(customer_pincode)
            # Find professionals in customer's pincode area
            professionals = Professional.query.filter(
                and_(
                    Professional.service_pincode == customer_pincode,
                    Professional.isActive == 1  # Only active professionals
                )
            ).all()
            profdata = Professional.query.filter_by(service_pincode=customer_pincode).all()
            print(f'prof-{profdata}')
            print( f'pro {professionals}')
            # Prepare results
            results = []
            for prof in professionals:
                # Get service details for each professional
                service = Services.query.filter_by(
                    service_id=prof.service_type
                ).first()
                
                # Filter based on search query if provided
                if search_query and not any([
                    search_query.lower() in service.service_name.lower(),
                    search_query.lower() in service.category.lower(),
                    search_query.lower() in service.description.lower() if service.description else False,
                    search_query.lower() in prof.fullname.lower()
                ]):
                    continue
                
                # Build service details
                service_details = {
                    'professional_id': prof.professional_id,
                    'professional_name': prof.fullname,
                    'contact': prof.contact,
                    'experience': prof.experience,
                    'kudos': prof.kudos,
                    'description': prof.description,
                    'profile_image': prof.profile_image,
                    'service_pincode' : prof.service_pincode,
                    'service_details': {
                        'service_id': service.service_id,
                        'name': service.service_name,
                        'category': service.category,
                        'description': service.description,
                        'price': service.price,
                        'time_required': service.time_required
                    }
                }
                print(results)
                results.append(service_details)
                
            
            return {
                'customer_pincode': customer_pincode,
                'total_results': len(results),
                'services': results
            }, 200

        except ValueError as e:
            return {'message': 'Invalid pincode format in address'}, 400
        except Exception as e:
            print(f"Error in service search: {str(e)}")
            return {'message': 'Internal server error'}, 500



class ServiceRequestApi(Resource):
    @jwt_required()
    @CacheManager.cached(timeout=60, key_prefix='request')
    def get(self, service_request_id=None):
        current_user = get_jwt_identity()

        if service_request_id:
            # Fetch a specific service request
            service_request = Service_request.query.get(service_request_id)
            if not service_request:
                return {"message": "Service request not found."}, 404, {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'http://localhost:8080'
                }

            # Fetch associated user details
            customer = User.query.get(service_request.customer_id)
            professional = User.query.get(service_request.professional_id)

            # Role-based access control
            if current_user['role'] == 1 and service_request.customer_id != current_user['userid']:
                return {"message": "Access denied."}, 403, {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'http://localhost:8080'
                }
            if current_user['role'] == 2 and service_request.professional_id != current_user['userid']:
                return {"message": "Access denied."}, 403, {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'http://localhost:8080'
                }

            service_request_data = service_request.to_dict()
            service_request_data['customer'] = customer.to_dict()
            service_request_data['professional'] = professional.to_dict()
            return service_request_data, 200, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:8080'
            }

        # Fetch all relevant service requests
        if current_user['role'] == 0:  # Admin
            service_requests = Service_request.query.all()
            print(service_requests)
        elif current_user['role'] == 1:  # Customer
            service_requests = Service_request.query.filter_by(customer_id=current_user['userid']).all()
        elif current_user['role'] == 2:  # Professional
            service_requests = Service_request.query.filter_by(professional_id=current_user['userid']).all()
        else:
            return {"message": "Access denied."}, 403, {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'http://localhost:8080'
                }

        service_requests_data = []
        for service_request in service_requests:
            customer = Customer.query.get(service_request.customer_id)
            professional = Professional.query.get(service_request.professional_id)
            service_request_data = service_request.to_dict()
            service_request_data['customer'] = customer.to_dict()
            service_request_data['professional'] = professional.to_dict()
            service_requests_data.append(service_request_data)

        return {"services": service_requests_data,
                "service-mapping" : serviceMapping}, 200, {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:8080',
            'Access-Control-Allow-Credentials': 'true'
        }

    @jwt_required()
    def put(self, service_request_id):
        """
        Update a service request status and remarks:
        - Professional: Can accept/reject requests
        - Customer: Can change status to IN_PROGRESS/COMPLETED and add remarks
        """
        current_user = get_jwt_identity()
        
        service_request = Service_request.query.get(service_request_id)
        if not service_request:
            return {"message": "Service request not found."}, 404

        # Verify access rights
        if current_user['role'] == 1 and service_request.customer_id != current_user['userid']:
            return {"message": "Access denied."}, 403
        if current_user['role'] == 2 and service_request.professional_id != current_user['userid']:
            return {"message": "Access denied."}, 403

        data = request.get_json()
        
        try:
            # Handle status updates
            if 'service_status' in data:
                new_status = data['service_status']
                
                # Validate status transitions
                if current_user['role'] == 2:  # Professional
                    if new_status not in ['ACCEPTED', 'REJECTED']:
                        return {"message": "Invalid status for professional."}, 400
                    if new_status == 'ACCEPTED':
                        print(new_status)
                        service_request.service_status = ServiceStatus.ASSIGNED
                    if new_status == 'REJECTED':
                        print(new_status)
                        service_request.service_status = ServiceStatus.REJECTED

                
                elif current_user['role'] == 1:  # Customer
                    print(new_status)
                    if new_status not in ['IN_PROGRESS', 'COMPLETED']:
                        return {"message": "Invalid status for customer."}, 400
                    
                    # Validate status transitions
                    if new_status == 'IN_PROGRESS': 
                        if service_request.service_status != ServiceStatus.ASSIGNED:
                            print(f'In assigned: {new_status} {service_request.service_status}')
                            return {"message": "Can only start service after professional acceptance."}, 400
                        if service_request.service_status == ServiceStatus.ASSIGNED:
                            print(new_status)
                            service_request.service_status = ServiceStatus.IN_PROGRESS

                    if new_status == 'COMPLETED':
                        if service_request.service_status != ServiceStatus.IN_PROGRESS:
                            return {"message": "Can only complete service that is in progress."}, 400
                        if service_request.service_status == ServiceStatus.IN_PROGRESS:
                            print(new_status)
  
                            service_request.service_status = ServiceStatus.COMPLETED
                            service_request.completed()
                            service_request.remarks = data['remarks']
                            service_request.ratings = data['ratingnum'] 

                            pro = Professional.query.get(service_request.professional_id)
                            pro.kudos = pro.kudos + analyze_sentiment(data.get('remarks'),float(data.get('ratingnum',0)))

                db.session.commit()
                CacheManager.clear_request_caches(request_id=service_request_id)
                return {"message": "Updated successfully"}, 200, {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'http://localhost:8080',
                    'Access-Control-Allow-Credentials': 'true'
                }
        except KeyError:
            return {"message": "Invalid status value."}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:8080'
            }


    @jwt_required()
    def post(self):
        """
        Create a new service request:
        - Only customers (role 1) can create new service requests
        """
        current_user = get_jwt_identity()

        # Only customers can create service requests
        if current_user['role'] != 1:
            return {"message": "Access denied. Only customers can create service requests."}, 403

        data = request.get_json()
        service_id = data.get('service_id')
        professional_id = data.get('professional_id')

        if not service_id :
            return {"message": "Missing required fields: 'service_id'."}, 400

        try:
            # Create a new service request
            new_request = Service_request(
                service_id=service_id,
                customer_id=current_user['userid'],
                professional_id=professional_id, 
                service_status=ServiceStatus.REQUESTED
            )

            db.session.add(new_request)
            db.session.commit()
            return {"message": "Created successfully"}, 201, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:8080',
                'Access-Control-Allow-Credentials': 'true'
            }
        except IntegrityError:
            db.session.rollback()
            return {"message": "Invalid service request data or service already requested."}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:8080'
            }


class AdminAnalyticsApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 0:
            return {"message": "Access denied"}, 403 ,{
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:8080'
            }

        try:
            # Get total counts
            total_customers = Customer.query.count()
        
            total_professionals = Professional.query.filter_by(isActive=1).count()
            total_services = Services.query.count()
            pending_verifications = Professional.query.filter_by(isActive=0).count()

            print(total_customers,total_professionals,total_services,pending_verifications)
            # Get service requests by status

            status_counts = db.session.query(
                Service_request.service_status,
                db.func.count(Service_request.service_request_id)
            ).group_by(Service_request.service_status).all()

            status_counts = {
                status.value: count 
                for status, count in status_counts
            }
            print(status_counts)

            # Get top services
            top_services_data = db.session.query(
                Services.service_name,
                db.func.count(Service_request.service_id).label('count')
            ).join(
                Service_request, Services.service_id == Service_request.service_id
            ).group_by(
                Services.service_id, Services.service_name  # Include service_name in GROUP BY
            ).order_by(
                db.func.count(Service_request.service_id).desc()
            ).limit(5).all()

            # Convert to dictionary
            top_services = {service_name: count for service_name, count in top_services_data}

            return {
                "summary": {
                    "total_customers": total_customers,
                    "total_professionals": total_professionals,
                    "total_services": total_services,
                    "pending_verifications": pending_verifications
                },
                "request_status": status_counts,
                "top_services": top_services
            }, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500, {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://localhost:8080'
            }




# @celery.tasks
# def generate_service_export():
#     try:
#         completed_requests = Service_request.query.filter_by(
#             service_status=ServiceStatus.COMPLETED
#         ).all()

#         output = io.StringIO()
#         writer = csv.writer(output)
        
#         writer.writerow([
#             'Service Request ID',
#             'Service ID',
#             'Customer ID',
#             'Professional ID',
#             'Date of Request',
#             'Date of Completion',
#             'Status',
#             'Remarks'
#         ])

#         for request in completed_requests:
#             writer.writerow([
#                 request.service_request_id,
#                 request.service_id,
#                 request.customer_id,
#                 request.professional_id,
#                 request.date_of_request,
#                 request.date_of_completion,
#                 request.service_status.value,
#                 request.remarks
#             ])

#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         filename = f'service_export_{timestamp}.csv'
#         filepath = os.path.join(LocalDevelopementConfig.UPLOAD_FOLDER, filename)
        
#         with open(filepath, 'w') as f:
#             f.write(output.getvalue())

#         return {
#             'status': 'success',
#             'filename': filename
#         }
#     except Exception as e:
#         return {
#             'status': 'error',
#             'message': str(e)
#         }




# class ServiceExportApi(Resource):
#     @jwt_required()
#     def post(self):
#         current_user = get_jwt_identity()
#         if current_user['role'] != 0:
#             return {"message": "Access denied"}, 403

#         # Trigger celery task
#         task = generate_service_export.delay()
#         return {"message": "Export started", "task_id": str(task.id)}, 202

#     @jwt_required()
#     def get(self, task_id):
#         current_user = get_jwt_identity()
#         if current_user['role'] != 0:
#             return {"message": "Access denied"}, 403

#         task_result = generate_service_export.AsyncResult(task_id)
#         if task_result.ready():
#             result = task_result.get()
#             if result['status'] == 'success':
#                 return {
#                     "status": "completed",
#                     "download_url": f"http://127.0.0.1:8000/documents/{result['filename']}"
#                 }
#             return {"status": "failed", "error": result['message']}
#         return {"status": "pending"}


























# class ServiceSearchAPI(Resource):
#     @jwt_required()
#     def get(self):
#         try:
#             # Get search query from URL parameters
#             search_query = request.args.get('query', '')
            
#             # Get current user's location from database
#             current_user = get_jwt_identity()
#             userflag, usertype = valid_user(current_user)

#             if(usertype != 'user'):
#                 return { 'message' : 'You are not authorized'} ,404
            
#             customerdata = Customer.query.filter_by(customer_id=current_user['userid']).first()

#             location = customerdata.primary_address.split(" ")[-1]
#             location = int(location)

#             professional = Professional.query.filter_by(service_pincode=location).all()
#             user_pincode = professional.service_pincode


