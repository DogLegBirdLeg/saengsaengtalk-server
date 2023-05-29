from flask import request
from flask_restx import Namespace, Resource
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer
from logic.user.application.port.incoming.AuthUseCase import AuthUseCase


logout_ns = Namespace('logout', description='로그아웃')


@logout_ns.route('')
class Logout(Resource):
    @logout_ns.doc(security='jwt', description="로그아웃")
    @logout_ns.response(code=204, description='로그아웃 성공')
    @inject
    def post(self, authentication_use_case: AuthUseCase = Provide[UserContainer.auth_service]):
        """로그아웃"""
        access_token = request.headers['Authorization']
        authentication_use_case.logout(access_token)
        return '', 204
