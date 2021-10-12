import pytest

from movie_app.app import app


@pytest.fixture
def flask_app():
    app.config['TESTING'] = True
    return app