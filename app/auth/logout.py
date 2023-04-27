from flask_restx import Namespace, Resource
from logic.user.use_case.AuthenticationUseCase import IAuthenticationUseCase

from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer

logout_ns = Namespace('logout', description='로그아웃')


@logout_ns.route('')
class Logout(Resource):
    @logout_ns.doc(security='jwt', description="로그아웃")
    @logout_ns.response(code=204, description='로그아웃 성공')
    @inject
    def delete(self, authentication_use_case: IAuthenticationUseCase = Provide[UserContainer.authentication_use_case]):
        """로그아웃"""
        authentication_use_case.logout()
        return '', 204
