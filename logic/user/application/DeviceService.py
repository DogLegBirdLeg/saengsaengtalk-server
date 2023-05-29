from logic.user.application.port.incoming.DeviceUseCase import DeviceUseCase
from logic.user.application.port.outgoing.DeviceDao import DeviceDao


class DeviceService(DeviceUseCase):
    def __init__(self, device_dao: DeviceDao):
        self.device_dao = device_dao

    def get_notification_allow(self, access_token):
        return self.device_dao.find_notification_allow_by_device_token(access_token)

    def append_device(self, user_id, access_token, device_token):
        self.device_dao.save(user_id, access_token, device_token)

    def update_notification_allow(self, access_token, allow):
        self.device_dao.update_notification_allow(access_token, allow)
