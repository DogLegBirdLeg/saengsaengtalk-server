from flask import Flask, g, request
from src.order_container import OrderContainer
from src.post_container import PostContainer
from src.store_container import StoreContainer
from src.comment_container import CommentContainer
from src.auth_container import AuthContainer
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import apidoc

URL_PREFIX = '/static'
apidoc.apidoc.url_prefix = URL_PREFIX


def create_app():
    auth_container = AuthContainer()
    order_container = OrderContainer()
    post_container = PostContainer()
    store_container = StoreContainer()
    comment_container = CommentContainer()

    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    from app.auth.auth_api import auth_bp
    app.register_blueprint(auth_bp)

    from app.api.delivery_api import delivery_bp
    app.register_blueprint(delivery_bp)

    @app.before_request
    def init_g():
        if "docs" in request.path or "swagger" in request.path:
            return

        if "/api/delivery" in request.path:
            g.id = request.headers['user_id']
            g.nickname = request.headers['nickname'].encode('iso-8859-1').decode('utf-8')

    return app
