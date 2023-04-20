import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from config.production.config import CRED_PATH

cred = credentials.Certificate(CRED_PATH)
firebase_admin.initialize_app(cred)

def push_message(tokens, message):
    message = messaging.MulticastMessage(tokens=tokens, data={
        'message': message
    })
    res = messaging.send_multicast(message)
    for response in res.responses:
        print(response.success)
