from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from logic.delivery.comment.application.CommentUseCase import CommentUseCase
from logic.delivery.comment.infra.CommentRepository import MongoDBCommentRepository
from logic.delivery.comment.infra.CommentDAO import MongoDBCommentDAO


class CommentContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.comment'])

    mongodb_connection = providers.Factory(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
    )

    comment_repository = providers.Factory(MongoDBCommentRepository, mongodb_connection)
    comment_dao = providers.Factory(MongoDBCommentDAO, mongodb_connection)
    comment_use_case = providers.Factory(CommentUseCase, comment_repository=comment_repository, comment_dao=comment_dao)
