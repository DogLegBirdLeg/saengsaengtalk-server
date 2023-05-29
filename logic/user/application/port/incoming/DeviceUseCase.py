from abc import *


class DeviceUseCase(metaclass=ABCMeta):
    @abstractmethod
    def append_device(self,user_id, access_token, device_token):
        pass

    @abstractmethod
    def get_notification_allow(self, access_token):
        pass

    @abstractmethod
    def update_notification_allow(self, access_token, allow):
        pass
