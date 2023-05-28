from abc import *


class DeviceDao(metaclass=ABCMeta):
    @abstractmethod
    def find_notification_allow_by_device_token(self, user_id, device_token):
        pass

    @abstractmethod
    def save(self, user_id, key, device_token):
        pass

    @abstractmethod
    def update_notification_allow(self, user_id, device_token, allow):
        pass
