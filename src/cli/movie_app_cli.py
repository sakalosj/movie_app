import logging

import click
from sqlalchemy import column
from sqlalchemy.dialects.postgresql import insert

from cli.web_scraper import get_movie_list
from app_config import DEFAULT_CONFIG_PATH, AppConfig
from db import db_session
from db.actor import ActorModel
from db.db_helpers import init_db, drop_db
from db.movie import MovieModel, movies2actors
from log import setup_logging

logger = logging.getLogger(__name__)
setup_logging(log_level='info')


@click.group()
def movie_app_cli():
    pass


@movie_app_cli.command()
@click.option('--config_file', default=DEFAULT_CONFIG_PATH, help='config file location')
def import_web_data(config_file):
    app_config = AppConfig.load_config(config_file)
    movie_list = get_movie_list(app_config.movie_app.data_url)
    with db_session() as s:
        movies = [dict(title=movie.title, link=movie.link) for movie in movie_list]
        inserted_movies = s.execute(
            insert(MovieModel).values(movies).on_conflict_do_nothing().returning(column('id'), column('link')))
        s.commit()

        actors = [dict(first_name=actor.first_name, last_name=actor.last_name, link=actor.link) for movie in movie_list
                  for actor in movie.actors]

        inserted_actors = s.execute(
            insert(ActorModel).values(actors).on_conflict_do_nothing().returning(column('id'), column('link')))
        s.commit()

        movies_link2id = {i[1]: i[0] for i in inserted_movies}
        actors_link2id = {i[1]: i[0] for i in inserted_actors}
        rel = [dict(movie_id=movies_link2id[movie.link], actor_id=actors_link2id[actor.link]) for movie in movie_list
               for actor in
               movie.actors]
        stmt = insert(movies2actors).values(rel)
        s.execute(stmt)
        s.commit()


@movie_app_cli.command()
def initdb():
    init_db()


@movie_app_cli.command()
def dropdb():
    drop_db()


if __name__ == '__main__':
    movie_app_cli()
