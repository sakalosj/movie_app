import logging

import sqlalchemy as sa
from sqlalchemy import or_

from db import Base
from db.db_utils import Unaccent

logger = logging.getLogger(__name__)


class ActorModel(Base):
    __tablename__ = "actors"

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String, index=True)
    last_name = sa.Column(sa.String, index=True, nullable=False)
    link = sa.Column(sa.String, unique=True, nullable=False)

    @classmethod
    def search_by(cls, string: str, fields: list):
        stmt = or_(False, *[Unaccent(field).ilike(f'%{string}%') for field in fields])
        result = cls.query.where(stmt)
        return result.all()

