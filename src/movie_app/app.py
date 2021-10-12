from flask import Flask

from db import db_session
from movie_app.views.actor import ActorView
from movie_app.views.movie import MovieView
from movie_app.views.search import SearchView
from app_config import app_config
from log import setup_logging

if app_config.is_logging_enabled():
    setup_logging()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


app.add_url_rule('/', view_func=SearchView.as_view('search_view'))
app.add_url_rule('/movies/<int:id_>', view_func=MovieView.as_view('movie_view'))
app.add_url_rule('/actors/<int:id_>', view_func=ActorView.as_view('actor_view'))


if __name__ == '__main__':
    app.run()
