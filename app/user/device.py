from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer
from flask import request, g
from bson import ObjectId
from logic.user.application.port.incoming.DeviceUseCase import DeviceUseCase


device_ns = Namespace('notification_allow', description='푸시 알림 허용')

notification_allow = device_ns.model('알림 허용', {
    'allow': fields.Boolean(description='허용여부'),
})

parser = device_ns.parser()
parser.add_argument('device_token', type=str, help='기기 토큰')


@device_ns.route('')
class Notification(Resource):
    @device_ns.doc(security='jwt', description='기기 정보를 추가합니다. 앱 실행시 호출되어야 하며 중복되는 기기 토큰이 있다면 무시합니다', body=device_ns.model('device', model={
        'key': fields.String(description='토큰 식별자', example=str(ObjectId())),
        'device_token': fields.String(description='기기 토큰')
    }))
    @device_ns.response(code=204, description='추가 성공')
    @inject
    def post(self, device_use_case: DeviceUseCase = Provide[UserContainer.device_service]):
        """기기 정보 추가 """
        data = request.get_json()
        device_use_case.append_device(g.id, data['key'], data['device_token'])
        return '', 204


@device_ns.route('/notification')
class Notification(Resource):
    @device_ns.doc(security='jwt', description='알림 허용 상태를 조회합니다', parser=parser)
    @device_ns.response(code=200, description='조회 성공', model=notification_allow)
    @inject
    def get(self, device_use_case: DeviceUseCase = Provide[UserContainer.device_service]):
        """알림 허용 상태 조회"""
        device_token = request.args['device_token']
        allow = device_use_case.get_notification_allow(g.id, device_token)
        return {'allow': allow}

    @device_ns.doc(security='jwt', description='알림 허용 상태를 변경합니다', body=device_ns.model('알림 허용 변경', {
        'device_token': fields.String(description='기기토큰'),
        'allow': fields.Boolean(description='허용여부'),
    }))
    @device_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, device_use_case: DeviceUseCase = Provide[UserContainer.device_service]):
        """알림 허용 상태 변경"""
        data = request.get_json()
        device_use_case.update_notification_allow(g.id, data['device_token'], data['allow'])
        return '', 204
