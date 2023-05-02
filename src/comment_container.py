from dependency_injector import containers, providers
from pymongo import MongoClient
from config.production import mongodb

from logic.delivery.comment.application.CommentQueryService import CommentQueryService
from logic.delivery.comment.application.CommentCreateService import CommentCreateService
from logic.delivery.comment.application.CommentDeleteService import CommentDeleteService
from logic.delivery.comment.adapter.outcoming.persistance.CommentRepository import MongoDBCommentRepository


class CommentContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['app.api.comment'])

    mongodb_connection = providers.Singleton(
        MongoClient,
        host=mongodb.host,
        username=mongodb.user,
        password=mongodb.pwd,
        port=mongodb.port,
        connect=False
    )

    comment_repository = providers.Singleton(MongoDBCommentRepository, mongodb_connection)

    comment_query_service = providers.Singleton(CommentQueryService, comment_repository=comment_repository)
    comment_create_service = providers.Singleton(CommentCreateService, comment_repository=comment_repository)
    comment_delete_service = providers.Singleton(CommentDeleteService, comment_repository=comment_repository)
