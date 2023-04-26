from logic.user.domain.Entity.User import User


class UserMapper:
    @staticmethod
    def mapping_user(user_json) -> User:
        user = User(_id=user_json['_id'],
                    name=user_json['name'],
                    nickname=user_json['nickname'],
                    username=user_json['username'],
                    pw=user_json['pw'],
                    account_number=user_json['account_number'],
                    email=user_json['email'])

        return user
