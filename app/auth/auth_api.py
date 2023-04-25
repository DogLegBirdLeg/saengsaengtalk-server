from app.auth.signup import signup_ns
from app.auth.signin import signin_ns
from app.auth.logout import logout_ns
#from app.auth.user import user_ns

from flask import Blueprint
from flask_restx import Api

from app.util.error_handling import error_handler

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_api = Api(auth_bp, title='auth', doc='/docs')
error_handler(auth_api)

auth_api.add_namespace(signup_ns)
auth_api.add_namespace(signin_ns)
auth_api.add_namespace(logout_ns)
#auth_api.add_namespace(user_ns)
