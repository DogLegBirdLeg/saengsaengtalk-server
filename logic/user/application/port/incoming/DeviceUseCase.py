from abc import *


class DeviceUseCase(metaclass=ABCMeta):
    @abstractmethod
    def append_device(self, user_id, key, device_token):
        pass

    @abstractmethod
    def get_notification_allow(self, user_id, device_token):
        pass

    @abstractmethod
    def update_notification_allow(self, user_id, device_token, allow):
        pass
