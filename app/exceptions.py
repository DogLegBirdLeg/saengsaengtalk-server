class BaseException(Exception):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    @property
    def json(self):
        return {
            'msg': self.msg,
            'code': self.code,
        }


class DatabaseError(BaseException):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistResource(DatabaseError):
    def __init__(self, msg='존재하지 않는 리소스', code=2):
        super().__init__(msg=msg, code=code)


class DuplicateKeyError(DatabaseError):
    def __init__(self, msg='중복 키 존재', code=3):
        super().__init__(msg=msg, code=code)


# Domain Error
class DomainError(BaseException):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


# 인증 에러
class AuthError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class AccessDenied(AuthError):
    def __init__(self, msg='접근 권한 없음', code=100):
        super().__init__(msg=msg, code=code)


class SigninFail(AuthError):
    def __init__(self, msg='아이디 혹은 비밀번호가 일치하지 않음', code=101):
        super().__init__(msg=msg, code=code)


class NotExistUser(SigninFail):
    def __int__(self, msg='존재하지 않는 유저', code=102):
        super().__init__(msg=msg, code=code)


class DuplicateUser(SigninFail):
    def __init__(self, msg='중복 유저 존재', code=103):
        super().__init__(msg=msg, code=code)


class PasswordMismatch(AuthError):
    def __init__(self, msg='비밀번호 불일치', code=104):
        super().__init__(msg=msg, code=code)


class NotValidAuthCode(AuthError):
    def __init__(self, msg='인증 코드 불일치', code=105):
        super().__init__(msg=msg, code=code)


# 토큰 에러
class TokenError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistToken(TokenError):
    def __init__(self, msg='존재하지 않는 토큰', code=200):
        super().__init__(msg=msg, code=code)


class TokenDecodeFail(TokenError):
    def __init__(self, msg='유효하지 않은 토큰', code=201):
        super().__init__(msg=msg, code=code)


class ExpiredToken(TokenError):
    def __init__(self, msg='만료된 토큰', code=202):
        super().__init__(msg=msg, code=code)


class NotIncludeAuthorization(TokenError):
    def __init__(self, msg='Authorization 필드 누락', code=203):
        super().__init__(msg=msg, code=code)


# Store
class StoreError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistStore(StoreError):
    def __init__(self, msg='가게 리소스 찾을 수 없음', code=300):
        super().__init__(msg=msg, code=code)


class NotExistMenu(StoreError):
    def __init__(self, msg='메뉴 리소스 찾을 수 없음', code=301):
        super().__init__(msg=msg, code=code)


# Post
class PostError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistPost(PostError):
    def __init__(self, msg='게시글 리소스 찾을 수 없음', code=400):
        super().__init__(msg=msg, code=code)


# Order
class OrderError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class ClosedPost(OrderError):
    def __init__(self, msg='참여가 마감된 게시글', code=500):
        super().__init__(msg=msg, code=code)


class OrderCompleted(OrderError):
    def __init__(self, msg='주문이 완료된 게시글', code=501):
        super().__init__(msg=msg, code=code)


class OrderConfirmed(OrderError):
    def __init__(self, msg='주문이 확정된 게시글', code=502):
        super().__init__(msg=msg, code=code)


class MaxMember(OrderError):
    def __init__(self, msg='최대 인원', code=503):
        super().__init__(msg=msg, code=code)


class OwnerQuit(OrderError):
    def __init__(self, msg='대표 유저 탈퇴', code=504):
        super().__init__(msg=msg, code=code)


class AlreadyJoinedUser(OrderError):
    def __init__(self, msg='참여 완료된 유저', code=505):
        super().__init__(msg=msg, code=code)


class NotJoinedUser(OrderError):
    def __init__(self, msg='참여하지 않은 유저', code=506):
        super().__init__(msg=msg, code=code)
