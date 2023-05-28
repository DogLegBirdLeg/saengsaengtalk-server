from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from flask import request


notification_allow_ns = Namespace('notification_allow', description='푸시 알림 허용')


@notification_allow_ns.route('')
class Notification(Resource):
    @notification_allow_ns.doc(description='알림 허용 상태를 변경합니다', body=notification_allow_ns.model('알림 허용', {
        'allow': fields.Boolean(description='허용여부'),
    }))
    @notification_allow_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self):
        """알림 허용 상태 변경"""
        data = request.get_json()
        return '', 204
