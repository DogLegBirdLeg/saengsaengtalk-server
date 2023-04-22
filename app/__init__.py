from flask import Flask, g, request
from app.src.container import Container
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_restx import apidoc

URL_PREFIX = '/static'
apidoc.apidoc.url_prefix = URL_PREFIX


def create_app():
    container = Container()

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
            #g.id = request.headers['user_id']
            #g.nickname = request.headers['nickname'].encode('iso-8859-1').decode('utf-8')
            g.id=11111111
            g.nickname='test'
    return app
