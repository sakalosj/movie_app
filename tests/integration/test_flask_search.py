import pytest
from bs4 import BeautifulSoup


@pytest.mark.parametrize('search_in, m_found, a_found', [
    pytest.param('search_in=movies&search_in=actor_first_name&search_in=actor_last_name', 5, 2,
                 id='movies-first_name-last_name'),
    pytest.param('search_in=movies&search_in=actor_first_name', 5, 1, id='movies-first_name'),
    pytest.param('search_in=movies&search_in=actor_last_name', 5, 1, id='movies-last_name'),
    pytest.param('search_in=movies', 5, 0, id='movies'),
    pytest.param('search_in=actor_first_name&search_in=actor_last_name', 0, 2, id='first_name-last_name'),
    pytest.param('search_in=actor_first_name', 0, 1, id='first_name'),
    pytest.param('search_in=actor_last_name', 0, 1, id='last_name'),

])
def test_search_in(post_form, init_db_with_data, search_in, m_found, a_found):
    page = post_form('/',
                     data='search=movie&'+ search_in)
    soup = BeautifulSoup(page.data, "html.parser")
    movies = soup.find('h3', text='Movies:').parent.find_all('a')
    actors = soup.find('h3', text='Actors:').parent.find_all('a')

    assert len(movies) == m_found
    assert len(actors) == a_found


@pytest.mark.parametrize('search_string, m_found', [
    pytest.param('mov', 5,  id='lower_substring'),
    pytest.param('Î', 5, id='upper_accent_substring'),
    pytest.param('móvIe', 5, id='mixed_substring'),
    pytest.param('Movie1', 1, id='mixed_fullstring'),
    pytest.param('----', 0, id='not-existent'),
    pytest.param('', 0, id='empty'),

])
def test_search_in(post_form, init_db_with_data, search_string, m_found):
    page = post_form('/',
                     data=f'search={search_string}&search_in=movies&search_in=actor_first_name&search_in=actor_last_name')
    soup = BeautifulSoup(page.data, "html.parser")
    movies = soup.find('h3', text='Movies:').parent.find_all('a')

    assert len(movies) == m_found
