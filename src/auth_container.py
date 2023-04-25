from dependency_injector import containers, providers
from pymongo import MongoClient
from redis import StrictRedis
from config.production import mongodb, redis


from logic.auth.infra.UserRepository import MongoDBUserRepository
from logic.auth.infra.UserDAO import MongoDBUserDAO
from logic.auth.use_case.SignupUseCase import SignupUseCase
from logic.auth.infra.TokenDAO import MongoDBTokenDAO

from logic.auth.infra.EmailSender import EmailSender
from logic.auth.infra.CodeCache import RedisCodeCache
from logic.auth.use_case.AuthenticationUseCase import JwtAuthenticationUseCase


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.auth.signup',
                                                            'app.auth.signin',
                                                            'app.auth.logout'])

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

    email_sender = providers.Singleton(EmailSender)
    code_cache = providers.Singleton(
        RedisCodeCache,
        redis_connection=redis_connection
    )

    signup_use_case = providers.Singleton(
        SignupUseCase,
        user_repository=user_repository,
        user_dao=user_dao,
        email_sender=email_sender,
        code_cache=code_cache
    )

    authentication_use_case = providers.Singleton(
        JwtAuthenticationUseCase,
        user_repository=user_repository,
        token_dao=token_dao
    )





