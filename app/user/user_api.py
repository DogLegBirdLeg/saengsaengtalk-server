from app.user.signup import signup_ns
from app.user.profile import profile_ns
from app.user.forgot import forgot_ns

from flask import Blueprint
from flask_restx import Api

from app.util.error_handling import error_handler

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

user_bp = Blueprint('user', __name__, url_prefix='/api/user')
user_api = Api(user_bp, authorizations=authorizations, title='user', description='유저 API', doc='/docs')
error_handler(user_api)

user_api.add_namespace(signup_ns, path='/signup')
user_api.add_namespace(profile_ns, path='/profile')
user_api.add_namespace(forgot_ns, path='/forgot')
