from abc import *


class MessagePusher(metaclass=ABCMeta):
    @abstractmethod
    def send(self, title, body, tokens):
        pass
