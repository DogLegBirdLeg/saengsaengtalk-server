from flask import Blueprint
from flask_restx import Api

from app.util.error_handling import delivery_error_handler, format_error

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'incoming': 'header',
        'name': 'Authorization'
    }
}

delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')
delivery_api = Api(delivery_bp, authorizations=authorizations, title='delivery', description='배달 API', doc='/docs')
delivery_error_handler(delivery_api)
format_error(delivery_api)

from app.api.store import store_ns
from app.api.post import post_ns
from app.api.order import order_ns
from app.api.comment import comment_ns

delivery_api.add_namespace(store_ns, path='/store')
delivery_api.add_namespace(post_ns, path='/post')
delivery_api.add_namespace(order_ns, path='/post')
delivery_api.add_namespace(comment_ns, path='/post')
