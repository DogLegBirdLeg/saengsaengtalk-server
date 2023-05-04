from flask import Flask, g, request
from src.order_container import OrderContainer
from src.post_container import PostContainer
from src.store_container import StoreContainer
from src.comment_container import CommentContainer
from src.user_container import UserContainer
from src.common_container import CommonContainer

from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import apidoc

URL_PREFIX = '/static'
apidoc.apidoc.url_prefix = URL_PREFIX


def create_app():
    user_container = UserContainer()
    order_container = OrderContainer()
    post_container = PostContainer()
    store_container = StoreContainer()
    comment_container = CommentContainer()
    common_container = CommonContainer()

    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from app.user.user_api import user_bp
    app.register_blueprint(user_bp)

    from app.auth.auth_api import auth_bp
    app.register_blueprint(auth_bp)

    from app.api.delivery_api import delivery_bp
    app.register_blueprint(delivery_bp)

    @app.before_request
    def init_g():
        try:
            g.id = int(request.headers['user_id'])
            g.nickname = request.headers['nickname'].encode('iso-8859-1').decode('utf-8')
        except KeyError:
            pass

    return app
