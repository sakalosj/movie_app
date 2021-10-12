from sqlalchemy.sql.functions import ReturnTypeFromArgs

from db import Base, engine


def init_db():
    from .actor import ActorModel
    from .movie import MovieModel

    Base.metadata.create_all(bind=engine)


def drop_db():
    from .actor import ActorModel
    from .movie import MovieModel

    Base.metadata.drop_all(bind=engine)

class Unaccent(ReturnTypeFromArgs):
    pass

# class BaseMixin: