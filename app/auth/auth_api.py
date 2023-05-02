from app.auth.login import login_ns
from app.auth.logout import logout_ns
from app.auth.refresh import refresh_ns
from flask import Blueprint
from flask_restx import Api

from app.util.error_handling import auth_error_handler

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'incoming': 'header',
        'name': 'Authorization'
    }
}

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_api = Api(auth_bp, authorizations=authorizations, title='auth', description='인증 API', doc='/docs')
auth_error_handler(auth_api)

auth_api.add_namespace(login_ns, path='/login')
auth_api.add_namespace(logout_ns, path='/logout')
auth_api.add_namespace(refresh_ns, path='/refresh')

