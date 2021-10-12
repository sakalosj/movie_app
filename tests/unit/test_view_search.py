from typing import List, Any, Iterable

import pytest

from movie_app.views.search import SearchView


@pytest.fixture
def mock_search_view(mocker, flask_app):
    def factory(search_in, search_str):
        search_form_mock = mocker.patch('movie_app.views.search.SearchForm')
        search_form_mock.return_value.search_in.data = search_in
        # set parameters to values which can be used to check if ActorModel.search_by was called with correct parameters
        search_form_mock.return_value.search.data = search_str

        with flask_app.test_request_context():
            mocker.patch('movie_app.views.search.request')

        movie_model_mck = mocker.patch('movie_app.views.search.MovieModel')
        actor_model_mck = mocker.patch('movie_app.views.search.ActorModel')

        actor_model_mck.first_name = 'actor_first_name'
        actor_model_mck.last_name = 'actor_last_name'
        mocker.patch('movie_app.views.search.render_template')

        return movie_model_mck, actor_model_mck

    return factory


test_data = [
    pytest.param(['movies', 'actor_first_name', 'actor_last_name'], 1, 1,
                 id='movies-first_name-last_name'),
    pytest.param(['movies', 'actor_first_name'], 1, 1, id='movies-first_name'),
    pytest.param(['movies', 'actor_last_name'], 1, 1, id='movies-last_name'),
    pytest.param(['movies'], 1, 0, id='movies'),
    pytest.param(['actor_first_name', 'actor_last_name'], 0, 1, id='first_name-last_name'),
    pytest.param(['actor_first_name'], 0, 1, id='first_name'),
    pytest.param(['actor_last_name'], 0, 1, id='last_name'),
    pytest.param([], 0, 0, id='empty'),

]


@pytest.mark.parametrize('search_in, m_called, a_called', test_data)
def test_post_search_in(mock_search_view, search_in, m_called, a_called):
    """
    Testing if correct queries were called. Should be improved by checking call parameter not differentiating between
    """
    search_str = '_'
    search_view = SearchView()

    movie_model_mck, actor_model_mck = mock_search_view(search_in, search_str)

    search_view.post()

    assert m_called == movie_model_mck.search_by_title.call_count
    assert a_called == actor_model_mck.search_by.call_count
    if a_called:
        search_in_args = [i for i in search_in if i != 'movies']
        assert actor_model_mck.search_by.call_args.args == (search_str, search_in_args)


@pytest.mark.parametrize('search_in, m_called, a_called', test_data)
def test_post_movie_model_calls(mock_search_view, search_in, m_called, a_called):
    """
    Testing if correct queries were called. Should be improved by checking call parameter not differentiating between
    """
    search_str = '_'
    search_view = SearchView()

    movie_model_mck, _ = mock_search_view(search_in, search_str)

    search_view.post()

    assert m_called == movie_model_mck.search_by_title.call_count


@pytest.mark.parametrize('search_in, m_called, a_called', test_data)
def test_post_actor_model_calls(mock_search_view, search_in, m_called, a_called):
    """
    Testing if correct queries were called. Should be improved by checking call parameter not differentiating between
    """
    search_str = '_'
    search_view = SearchView()

    _, actor_model_mck = mock_search_view(search_in, search_str)

    search_view.post()

    actor_model_call_args = [i for i in search_in if i != 'movies']

    if a_called:
        actor_model_mck.search_by.assert_called_once_with(search_str, actor_model_call_args)
    else:
        actor_model_mck.search_by.assert_not_called()
