from http import HTTPStatus
from app import exceptions


def error_handler(api):
    @api.errorhandler(exceptions.TokenDecodeFail)
    def decode_error_handling(error):
        return error.json, 401

    @api.errorhandler(exceptions.ExpiredToken)
    def expired_token_handling(error):
        return error.json, 401

    @api.errorhandler(exceptions.NotIncludeAuthorization)
    def not_include_authorization(error):
        return error.json, 401

    @api.errorhandler(exceptions.AccessDenied)
    def access_denied(error):
        return error.json, 403

    @api.errorhandler(exceptions.NotValidAuthCode)
    def not_valid_auth_code(error):
        return error.json, 401

    @api.errorhandler(exceptions.NotExistPost)
    def access_denied(error):
        return error.json, 404

    @api.errorhandler(exceptions.NotExistStore)
    def not_exist_store_handling(error):
        return error.json, 404

    @api.errorhandler(exceptions.NotExistMenu)
    def not_exist_store_handling(error):
        return error.json, 404

    @api.errorhandler(exceptions.CantModify)
    def cant_modify_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotRecruiting)
    def not_recruiting_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.AlreadyJoinedUser)
    def already_joined_user_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotJoinedUser)
    def not_joined_user_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.OwnerQuit)
    def owner_quit_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.MaxMember)
    def max_member_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotValidStatus)
    def not_valid_status_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotValidOrder)
    def not_valid_order_handling(error):
        return error.json, 406
