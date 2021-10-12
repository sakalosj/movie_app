from pathlib import Path
from unittest.mock import ANY

import pytest
from cli.web_scraper import get_movie_list, parse_movie


@pytest.fixture
def page_source():
    def pick_source(choice: str) -> str:
        if choice == 'main':
            return Path('./tests/data/source_data.html').read_text()
    return pick_source


@pytest.fixture
def tp_mock(mocker):
    """
    mocks ThreadPoolExecutor
    """
    mock = mocker.patch('cli.web_scraper.ThreadPoolExecutor')
    return mock


def test_get_movie_list(mocker, page_source, tp_mock):
    p = page_source('main')
    mock_gurl = mocker.patch('cli.web_scraper.get_url_content')
    mock_gurl.return_value = p
    mocker.patch('cli.web_scraper.BeautifulSoup')

    get_movie_list('_')
    assert tp_mock().__enter__().map.called_once_with(parse_movie, ANY)
