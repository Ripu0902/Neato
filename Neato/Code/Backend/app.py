# app.py
import os
from flask import Flask
from application.config import LocalDevelopementConfig
from application.database import db
from flask_restful import Api
from flask_jwt_extended import JWTManager
import logging
from application.celery_config import make_celery
from flask import send_from_directory
from flask_cors import CORS
from application.utils import CacheManager


logging.basicConfig(filename='debug.log',level=logging.DEBUG,format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = None
api = None


def create_app():
    app = Flask(__name__)

    if os.getenv('ENV',"developement") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting local developement")
        app.config.from_object(LocalDevelopementConfig)



    app.config.update(
        CACHE_TYPE="redis",
        CACHE_REDIS_HOST="localhost",
        CACHE_REDIS_PORT=6379,
        CACHE_REDIS_DB=0,
        CACHE_DEFAULT_TIMEOUT=300,
        CACHE_KEY_PREFIX="neato_"
    )

    if not os.path.exists(LocalDevelopementConfig.UPLOAD_FOLDER):
        os.makedirs(LocalDevelopementConfig.UPLOAD_FOLDER)

    app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    app.config["CELERY_BACKEND"] = "redis://localhost:6379/0"
    celery = make_celery(app)


    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    CacheManager.init_app(app)
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    
    app.app_context().push()
    # with app.app_context():
    db.create_all()

    from application.database import User, Roles  # Import your User and Role models here
    with app.app_context():
        # Ensure roles exist
        roles = [
            {"role_id": 0, "role_name": "admin"},
            {"role_id": 1, "role_name": "customer"},
            {"role_id": 2, "role_name": "professional"},
        ]

        for role_data in roles:
            if not Roles.query.filter_by(role_id=role_data["role_id"]).first():
                new_role = Roles(role_id=role_data["role_id"], role_name=role_data["role_name"])
                db.session.add(new_role)
                print(f"Role '{role_data['role_name']}' added.")

        db.session.commit()

        # Ensure an admin user exists
        if not User.query.filter_by(role=0).first():  # Check if an admin exists
            admin_user = User(
                username="admin",
                password="admin123",  # Make sure to hash the password before saving
                role=0  # Link to the admin role
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")

    return app, api , jwt , celery


app, api,jwt, celery = create_app()


from application.api import CustomerSignupApi,ProfessionalSignupApi, LoginApi,ServiceApi, VerifyProfessionalApi,UserDetails,ServiceRequestApi,AdminApi,ToggleBlockApi, ServiceSearchAPI,AdminAnalyticsApi

api.add_resource(CustomerSignupApi,"/api/customer-signup")
api.add_resource(LoginApi,"/api/login")
api.add_resource(UserDetails, '/api/user')
api.add_resource(AdminApi,'/api/get-user', '/api/get-user/<string:user_id>')
api.add_resource(ToggleBlockApi, '/api/toggle-block/<string:user_id>')
api.add_resource(VerifyProfessionalApi, "/api/verify-professional/<string:professional_id>")
api.add_resource(ServiceApi,"/api/create-service", '/api/service/<string:service_id>', '/api/services')
api.add_resource(ProfessionalSignupApi, "/api/professional-signup")
api.add_resource(ServiceSearchAPI, '/api/services/search')
api.add_resource(ServiceRequestApi,'/api/service-request','/api/service-request/<int:service_request_id>')
api.add_resource(AdminAnalyticsApi, '/api/admin/analytics')
# api.add_resource(ServiceExportApi, '/api/export-services', '/api/export-services/<string:task_id>')


@app.route('/documents/<path:filename>')
def serve_document(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )