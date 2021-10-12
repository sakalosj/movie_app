from flask import render_template, abort
from flask.views import MethodView
from sqlalchemy.exc import NoResultFound

from db.movie import MovieModel


class MovieView(MethodView):
    def get(self, id_: int):
        try:
            movie = MovieModel.query.filter_by(id=id_).one()
        except NoResultFound:
            abort(404, 'Item not found')

        return render_template('movie.html', movie=movie)
