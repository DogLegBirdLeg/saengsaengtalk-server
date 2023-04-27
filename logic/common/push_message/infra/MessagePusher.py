import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from config.production.config import CRED_PATH
from logic.common.push_message.infra.TokenDAO import ITokenDAO

from logic.common.push_message.application.IMessagePuhser import IMessagePusher

cred = credentials.Certificate(CRED_PATH)
firebase_admin.initialize_app(cred)


class MessagePusher(IMessagePusher):
    def __init__(self, token_dao: ITokenDAO):
        self.token_dao = token_dao

    def push(self, users, title, body):
        tokens = self.token_dao.find_all_registration_token_user_id(users)

        message = messaging.MulticastMessage(
            tokens=tokens,
            notification=messaging.Notification(
                title=title,
                body=body
            )
        )
        res = messaging.send_multicast(message)
