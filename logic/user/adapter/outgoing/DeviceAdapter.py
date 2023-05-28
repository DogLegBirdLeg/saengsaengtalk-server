import pymongo.errors
from datetime import datetime
import exceptions
from bson import ObjectId
from logic.user.application.port.outgoing.DeviceDao import DeviceDao


class MongoDBDeviceDao(DeviceDao):
    def __init__(self, mongodb_connection):
        self.db = mongodb_connection['auth']

    def find_notification_allow_by_device_token(self, user_id, device_token):
        find = {
            'user_id': user_id,
            'device_token': device_token
        }
        device = self.db.device.find_one(find)
        if device is None:
            raise exceptions.NotExistResource

        return device['notification_allow']

    def save(self, user_id, key, device_token):
        data = {
            'user_id': user_id,
            'key': ObjectId(key),
            'device_token': device_token,
            'notification_allow': False,
            'last_updated_date': datetime.now()
        }

        try:
            self.db.device.insert_one(data)
        except pymongo.errors.DuplicateKeyError:  # 중복 키 에러 발생시 무시
            find = {
                'device_token': device_token
            }

            data = {
                '$set': {'last_updated_date': datetime.now()}
            }
            self.db.device.update_one(find, data)

    def update_notification_allow(self, user_id, device_token, allow):
        find = {
            'user_id': user_id,
            'device_token': device_token
        }

        data = {
            '$set': {
                'notification_allow': allow
            }
        }

        self.db.device.update_one(find, data)
