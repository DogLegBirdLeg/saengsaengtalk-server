from app.auth.Domain.Entity.Token import Token


class TokenMapper:
    @staticmethod
    def mapping_token(token_json) -> Token:
        token = Token(user_id=token_json['user_id'],
                      access_token=token_json['access_token'],
                      refresh_token=token_json['refresh_token'],
                      registration_token=token_json['registration_token'])

        return token
