import logging
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import List

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests import Response

from app_config import app_config
from log import setup_logging

logger = logging.getLogger(__name__)


@dataclass
class Movie:
    title: str
    actors: list
    link: str
    rank: int


@dataclass
class Actor:
    full_name: str
    first_name: str = field(init=False)
    last_name: str = field(init=False)
    link: str

    def __post_init__(self):
        self.last_name, self.first_name, *_ = re.split(r'\s', self.full_name, 1)[::-1] + [None]


def get_movie_list(url: str) -> List[Movie]:
    """
    Function returns list of movies parsed from provided url.
    """
    page = get_url_content(url)
    logger.info('Parsing movie list page source')
    soup = BeautifulSoup(page, "html.parser")

    movies = soup.find_all('div', 'article-content-toplist')

    logger.info('Starting parallel movie data scrapping')
    with ThreadPoolExecutor(max_workers=100) as exe:
        results = exe.map(parse_movie, movies)

    return list(results)


def get_url_content(url: str) -> str:
    """
    Function gets html document from provided url
    """
    logger.info(f'Getting content of {url}')
    header = {'User-Agent': UserAgent().chrome}
    return requests.get(url, headers=header).content


def parse_movie(movie) -> Movie:
    logger.info(f'Processing movie {movie.a.get("title")}')
    title = movie.a.get('title')
    link = movie.a.get('href')
    actors = get_actors_from_details(link, title)
    rank = int(movie.span.text.strip('.'))
    return Movie(title=title, actors=actors, link=link, rank=rank)


def get_actors_from_details(url_suffix: str, title: str) -> List[Actor]:
    logger.info(f'Getting actor list from movie {title} details')

    page = get_url_content(f'https://www.csfd.cz{url_suffix}')
    soup = BeautifulSoup(page, "html.parser")
    actors = soup.find('h4', text='Hrají: ').parent.find_all('a')[:-1]
    return [Actor(full_name=actor.text, link=actor.get('href')) for actor in actors]


if __name__ == '__main__':
    setup_logging(log_level='info')
    get_movie_list(app_config.movie_app.data_url)
