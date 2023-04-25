from flask import request
from flask_restx import Resource, Namespace, fields
from logic.auth.use_case.SignupUseCase import SignupUseCase
from app import exceptions
from dependency_injector.wiring import inject, Provide
from src.auth_container import AuthContainer

signup_ns = Namespace('signup', description='회원가입 API')


duplicate_result_model = signup_ns.model("중복 여부", {
    'is_duplicated': fields.Boolean(description="중복 여부")
})

signup_format_model = signup_ns.model('회원가입', {
    'auth_code': fields.String(description='인증 코드', example='MiryangCampus2023'),
    'name': fields.String(description='이름', required=True, example='김개발'),
    'username': fields.String(description='유저 ID', required=True, example='milcampus1234'),
    'pw': fields.String(description='비밀번호', required=True, example='dogLegBirdLeg1234'),
    'nickname': fields.String(description='닉네임', required=True, example='개발이'),
    'account_number': fields.String(description='계좌번호', required=True, example='123-1234-123456 농협'),
    'email': fields.String(description='이메일', required=True, example='milcampus1234@naver.com')
})

parser = signup_ns.parser()
parser.add_argument('field', type=str, help='중복을 검사할 필드', choices=('username', 'nickname'))
parser.add_argument('value', type=str, help='중복을 검사할 값')


@signup_ns.route('/duplicate-check')
class UsernameCheck(Resource):
    @signup_ns.doc(parser=parser, description="필드의 값이 중복되는지 검사합니다")
    @signup_ns.response(code=200, description="검사 결과", model=duplicate_result_model)
    @inject
    def get(self, signup_use_case: SignupUseCase = Provide[AuthContainer.signup_use_case]):
        is_duplicated = signup_use_case.check_field(request.args['field'], request.args['value'])

        return {'is_duplicated': is_duplicated}


email_parser = signup_ns.parser()
email_parser.add_argument('email', type=str, help='이메일')


@signup_ns.route('')
class Signup(Resource):
    @signup_ns.doc(parser=email_parser, description="인증코드 전송 요청")
    @signup_ns.response(code=201, description='요청 성공')
    @inject
    def get(self, signup_use_case: SignupUseCase = Provide[AuthContainer.signup_use_case]):
        email = request.args['email']

        signup_use_case.send_auth_email(email)
        return '', 201

    @signup_ns.doc(description="회원가입")
    @signup_ns.expect(signup_format_model)
    @signup_ns.response(code=201, description='가입 성공')
    @inject
    def post(self, signup_use_case: SignupUseCase = Provide[AuthContainer.signup_use_case]):
        data = request.get_json()

        try:
            signup_use_case.signup(data['auth_code'], data['name'], data['username'], data['pw'], data['nickname'], data['account_number'], data['email'])
        except exceptions.DuplicateUser as error:
            return error.json, 409

        return '', 201
