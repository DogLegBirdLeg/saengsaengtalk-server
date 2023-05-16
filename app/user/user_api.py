from app.user.signup import signup_ns
from app.user.profile import profile_ns
from app.user.forgot import forgot_ns
from app.user.user import duplicate_check_ns

from flask import Blueprint
from flask_restx import Api

from app.util.error_handling import user_error_handling, format_error

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'incoming': 'header',
        'name': 'Authorization'
    }
}

user_bp = Blueprint('user', __name__, url_prefix='/user')
user_api = Api(user_bp, authorizations=authorizations, title='user', description='유저 API', doc='/docs')
user_error_handling(user_api)
format_error(user_api)

user_api.add_namespace(signup_ns, path='/signup')
user_api.add_namespace(profile_ns, path='/profile')
user_api.add_namespace(forgot_ns, path='/forgot')
user_api.add_namespace(duplicate_check_ns, path='/duplicate-check')


parser = signup_ns.parser()
parser.add_argument('field', type=str, help='중복을 검사할 필드', choices=('username', 'nickname'))
parser.add_argument('value', type=str, help='중복을 검사할 값')


