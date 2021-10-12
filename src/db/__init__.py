from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app_config import app_config

engine = create_engine(app_config.db_url)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine)
                            )


class Base:
    def __repr__(self):

        params = ', '.join(f'{k}={v}' for k, v in self._keyvalgen(self))
        return f"{self.__class__.__name__}({params})"

    @staticmethod
    def _keyvalgen(obj):
        """ Generate attr name/val pairs, filtering out SQLA attrs."""
        excl = ('_sa_adapter', '_sa_instance_state')
        for k, v in vars(obj).items():
            if not k.startswith('_') and not any(hasattr(v, a) for a in excl):
                yield k, v


Base = declarative_base(cls=Base)

Base.query = db_session.query_property()

from .movie import MovieModel
from .actor import ActorModel