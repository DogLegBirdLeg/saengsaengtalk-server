from abc import *


class IMessagePusher(metaclass=ABCMeta):
    @abstractmethod
    def push(self, users, title, body):
        pass
