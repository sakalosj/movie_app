import logging

import click
from sqlalchemy import column
from sqlalchemy.dialects.postgresql import insert

from cli.cli_utils import _insert_movies, _insert_actors, _insert_relations
from cli.web_scraper import get_movie_list
from app_config import DEFAULT_CONFIG_PATH, AppConfig
from db import db_session
from db.actor import ActorModel
from db.db_utils import init_db, drop_db
from db.movie import MovieModel, movies2actors
from log import setup_logging

logger = logging.getLogger(__name__)
setup_logging(log_level='info')


@click.group()
def movie_app_cli():
    pass


@movie_app_cli.command()
@click.option('--config_file', default=DEFAULT_CONFIG_PATH, help='Config file location')
def import_web_data(config_file):
    """
        Imports data from web to db
    """
    app_config = AppConfig.load_config(config_file)
    movie_list = get_movie_list(app_config.movie_app.data_url)
    with db_session() as s:
        inserted_movies = _insert_movies(s, movie_list)
        inserted_actors = _insert_actors(s, movie_list)
        _insert_relations(s, movie_list, inserted_movies, inserted_actors)


@movie_app_cli.command()
def initdb():
    """
    Initialize db
    """
    init_db()


@movie_app_cli.command()
def dropdb():
    """
    Drops db
    """
    drop_db()


if __name__ == '__main__':
    movie_app_cli()
