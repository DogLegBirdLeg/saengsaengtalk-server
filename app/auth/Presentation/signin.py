from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource, fields
from app.auth.Service.AuthService import AuthService
from app import exceptions
from dependency_injector.wiring import inject, Provide
from app.src.container import Container

signin_ns = Namespace('signin', description='로그인 API')

signin_format_model = signin_ns.model('로그인 포멧', {
    'username': fields.String(description='유저 ID', example='milcampus1234'),
    'pw': fields.String(description='비밀번호', example='dogLegBirdLeg1234'),
    'registration_token': fields.String(description='기기 토큰')
})
signin_result_model = signin_ns.model('로그인 결과', {
    'user_id': fields.Integer(description='유저 식별 번호', example='1679129293081'),
    'nickname': fields.String(description='닉네임', example='개발이')
})


@signin_ns.route('')
class Signin(Resource):
    @signin_ns.doc(description="로그인")
    @signin_ns.expect(signin_format_model)
    @signin_ns.response(code=200, description='로그인 결과', model=signin_result_model, headers={'Authentication': 'access_token/refresh_token'})
    @inject
    def post(self, auth_service: AuthService = Provide[Container.auth_service]):
        data = request.get_json()

        try:
            token, user = auth_service.signin(data['username'], data['pw'], data['registration_token'])
        except exceptions.NotExistUser:
            error = exceptions.SigninFail()
            return error.json, 401

        except exceptions.PasswordMismatch:
            error = exceptions.SigninFail()
            return error.json, 401

        res = jsonify(user_id=user._id, nickname=user.nickname)
        res.headers['Authentication'] = f'{token.access_token}/{token.refresh_token}'

        return res


parser = signin_ns.parser()
parser.add_argument('Authorization', type=str, location='headers', help='Refresh Token')


@signin_ns.route('/refresh')
class Refresh(Resource):
    @signin_ns.doc(parser=parser, description="access token 토큰 갱신")
    @signin_ns.response(code=200, description='갱신 성공', headers={'Authentication': 'access_token'})
    @inject
    def get(self, auth_service: AuthService = Provide[Container.auth_service]):
        refresh_token = request.headers['Authorization']

        access_token = auth_service.refresh(refresh_token)

        res = make_response()
        res.headers['Authentication'] = f'{access_token}'

        return res
