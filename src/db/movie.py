import sqlalchemy as sa
from sqlalchemy.orm import relationship
from unidecode import unidecode

from db import Base
from db.db_helpers import Unaccent

movies2actors = sa.Table('movies2actors', Base.metadata,
    sa.Column('movie_id', sa.ForeignKey('movies.id')),
    sa.Column('actor_id', sa.ForeignKey('actors.id'))
)


class MovieModel(Base):
    __tablename__ = 'movies'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String, nullable=False, index=True)
    link = sa.Column(sa.String, unique=True)

    actors = relationship(
        'ActorModel',
        secondary=movies2actors,
        backref='movies')

    @classmethod
    def search_by_title(cls, str):
        result = cls.query.filter(Unaccent(cls.title).ilike(f'%{unidecode(str)}%'))
        return result.all()