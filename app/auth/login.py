from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer
from bson import ObjectId
from app.util import validator

from logic.user.application.port.incoming.AuthUseCase import AuthUseCase


login_ns = Namespace('login', description='로그인')


@login_ns.route('')
class Login(Resource):
    @login_ns.doc(description="로그인")
    @login_ns.expect(login_ns.model('로그인 포멧', {
        'username': fields.String(description='유저 ID', example='milcampus1234'),
        'pw': fields.String(description='비밀번호', example='dogLegBirdLeg1234'),
    }))
    @login_ns.response(code=200, description='로그인 성공', headers={'Authentication': 'access_token/refresh_token'}, body=login_ns.model('login res', model={
        'key': fields.String(description='토큰 식별자', example=str(ObjectId()))
    }))
    @inject
    def post(self, authentication_use_case: AuthUseCase = Provide[UserContainer.auth_service]):
        """로그인"""
        data = request.get_json()
        username = data['username']
        password = data['pw']

        validator.validate_username(username)
        validator.validate_password(password)

        key, access_token, refresh_token = authentication_use_case.login(username, password)

        res = jsonify(key=key)
        res.headers['Authentication'] = f'{access_token}/{refresh_token}'
        return res
