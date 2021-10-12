from typing import List, Dict, Tuple

from sqlalchemy import column
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from cli.web_scraper import Movie
from db import MovieModel, ActorModel
from db.movie import movies2actors


def _insert_movies(s: Session, movie_list: List[Movie]) -> List[Tuple[int, int]]:
    """
    Inserts movies into db
    """
    movies = [dict(title=movie.title, link=movie.link) for movie in movie_list]
    inserted_movies = s.execute(
        insert(MovieModel).values(movies).on_conflict_do_nothing().returning(column('id'), column('link')))
    s.commit()
    return [(id_, link) for id_, link in inserted_movies]


def _insert_actors(s: Session, movie_list: List[Movie]) -> List[Tuple[int, int]]:
    """
    Inserts actors into db
    """
    actors = [dict(first_name=actor.first_name, last_name=actor.last_name, link=actor.link) for movie in movie_list
              for actor in movie.actors]
    inserted_actors = s.execute(
        insert(ActorModel).values(actors).on_conflict_do_nothing().returning(column('id'), column('link')))
    s.commit()
    return [(id_, link) for id_, link in inserted_actors]


def _insert_relations(s: Session, movie_list: List[Movie], inserted_movies, inserted_actors):
    """
    Genrates and inserts into db movie <-> actor relation
    """
    movies_link2id = {i[1]: i[0] for i in inserted_movies}
    actors_link2id = {i[1]: i[0] for i in inserted_actors}

    rel = [dict(movie_id=movies_link2id[movie.link], actor_id=actors_link2id[actor.link]) for movie in movie_list if
           movie.link in movies_link2id
           for actor in
           movie.actors]

    stmt = insert(movies2actors).values(rel).on_conflict_do_nothing()
    s.execute(stmt)
    s.commit()
