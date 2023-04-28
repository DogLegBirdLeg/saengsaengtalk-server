from dependency_injector import containers, providers
from pymongo import MongoClient
from redis import StrictRedis
from config.production import mongodb, redis


from logic.user.infra.UserRepository import MongoDBUserRepository
from logic.user.infra.UserDAO import MongoDBUserDAO
from logic.user.infra.TokenDAO import MongoDBTokenDAO

from logic.common.email.infra.EmailSender import EmailSender
from logic.common.cache.infra.CodeCache import RedisCodeCache
from logic.user.use_case.AuthenticationUseCase import JwtAuthentication
from logic.user.use_case.SignupUseCase import SignupUseCase, SignupEmailUseCase
from logic.user.use_case.ForgotUseCase import ForgotEmailSendUseCase, ForgotTempTokenPublishUseCase
from logic.user.use_case.ProfileUseCase import ProfileQueryUseCase, ProfileDeleteUseCase, ProfileUpdateUseCase
from logic.user.use_case.UserUseCase import UserUseCase


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.user.forgot',
                                                            'app.user.profile',
                                                            'app.user.signup',
                                                            'app.user.user',
                                                            'app.auth.login',
                                                            'app.auth.logout',
                                                            'app.auth.refresh'])

    redis_connection = providers.Singleton(
        StrictRedis,
        host=redis.host,
        port=redis.port,
        password=redis.pwd,
        db=redis.post_db,
        decode_responses=True
    )

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
        connect=False
    )

    user_repository = providers.Singleton(
        MongoDBUserRepository,
        mongodb_connection=mongodb_connection
    )

    user_dao = providers.Singleton(
        MongoDBUserDAO,
        mongodb_connection=mongodb_connection
    )

    token_dao = providers.Singleton(
        MongoDBTokenDAO,
        mongodb_connection=mongodb_connection
    )

    email_sender = providers.Factory(EmailSender)
    code_cache = providers.Singleton(
        RedisCodeCache,
        redis_connection=redis_connection
    )

    signup_use_case = providers.Singleton(
        SignupUseCase,
        user_repository=user_repository,
        code_cache=code_cache
    )

    signup_email_send_use_case = providers.Singleton(
        SignupEmailUseCase,
        email_sender=email_sender,
        code_cache=code_cache
    )

    authentication_use_case = providers.Singleton(
        JwtAuthentication,
        user_repository=user_repository,
        token_dao=token_dao
    )

    forgot_email_send_use_case = providers.Singleton(
        ForgotEmailSendUseCase,
        code_cache=code_cache,
        email_sender=email_sender,
        user_repository=user_repository
    )

    forgot_temp_token_publish_use_case = providers.Singleton(
        ForgotTempTokenPublishUseCase,
        code_cache=code_cache,
        user_repository=user_repository
    )

    profile_query_use_case = providers.Singleton(
        ProfileQueryUseCase,
        user_repository=user_repository,
        user_dao=user_dao
    )

    profile_delete_use_case = providers.Singleton(
        ProfileDeleteUseCase,
        user_repository=user_repository,
        user_dao=user_dao
    )

    profile_update_use_case = providers.Singleton(
        ProfileUpdateUseCase,
        user_repository=user_repository,
        user_dao=user_dao
    )

    user_use_case = providers.Singleton(
        UserUseCase,
        user_dao=user_dao
    )








