import os

import pytest
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app_config import AppConfig
from db import Base, MovieModel, ActorModel

@pytest.fixture
def app_config():
    return AppConfig.load_config(os.getenv('MOVIE_CFG', 'tests/data/test_movie_app.yaml'))

@pytest.fixture
def sa_engine(app_config):
    """
    Fixture to provide sqlalchemy engine
    """
    return create_engine(app_config.db_url)


@pytest.fixture
def sa_session(sa_engine):
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=sa_engine))


@pytest.fixture
def init_db(sa_engine, sa_session):
    """
    Fixture to cleanup db
    """
    with sa_engine.begin() as conn:
        Base.metadata.drop_all(bind=sa_engine)
        Base.metadata.create_all(bind=sa_engine)


@pytest.fixture
def db_data():
    PATH = './tests/data/db_data.yaml'
    with open(PATH, 'r') as file_:
        db_data: dict = yaml.safe_load(file_)
    return db_data


@pytest.fixture
def init_db_with_data(init_db, sa_session, db_data):
    movies = [MovieModel(**movie) for movie in db_data['movies']]
    actors = [ActorModel(**actor) for actor in db_data['actors']]

    with sa_session() as s:
        s.add_all(movies + actors)
        s.commit()

