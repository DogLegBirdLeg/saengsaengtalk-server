class StoreSummary:
    def __init__(self, _id, name, fee, min_order, phone_number, note):
        self._id = _id
        self.name = name
        self.fee = fee
        self.min_order = min_order
        self.phone_number = phone_number
        self.note = note

    @property
    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'fee': self.fee,
            'min_order': self.min_order,
            'phone_number': self.phone_number,
            'note': self.note
        }

    @staticmethod
    def mapping(store_summary_json):
        return StoreSummary(_id=store_summary_json['_id'],
                            name=store_summary_json['name'],
                            fee=store_summary_json['fee'],
                            min_order=store_summary_json['min_order'],
                            phone_number=store_summary_json['phone_number'],
                            note=store_summary_json['note'])


class Post:
    def __init__(self, _id, store_summary: StoreSummary, user_id, nickname, status, place, order_time, min_member, max_member, users):
        self._id = _id
        self.store_summary = store_summary
        self.user_id = user_id
        self.nickname = nickname
        self.status = status
        self.place = place
        self.order_time = order_time
        self.min_member = min_member
        self.max_member = max_member
        self.users = users

    @property
    def json(self):
        return {
            '_id': self._id,
            'store': self.store_summary.json,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'status': self.status,
            'place': self.place,
            'order_time': self.order_time,
            'min_member': self.min_member,
            'max_member': self.max_member,
            'users': self.users
        }

    @staticmethod
    def mapping(post_json):
        return Post(_id=post_json['_id'],
                    store_summary=StoreSummary.mapping(post_json['store']),
                    user_id=post_json['user_id'],
                    nickname=post_json['nickname'],
                    status=post_json['status'],
                    place=post_json['place'],
                    order_time=post_json['order_time'],
                    min_member=post_json['min_member'],
                    max_member=post_json['max_member'],
                    users=post_json['users'])
