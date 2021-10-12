import functools
import os

import pytest
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app_config import AppConfig
from db import Base, MovieModel, ActorModel
from movie_app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def post_form(client):
    return functools.partial(client.post, headers={'Content-Type': 'application/x-www-form-urlencoded'})




