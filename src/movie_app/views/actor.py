from flask import render_template, abort
from flask.views import MethodView
from sqlalchemy.exc import NoResultFound

from db.actor import ActorModel


class ActorView(MethodView):
    def get(self, id_: int):

        try:
            actor = ActorModel.query.filter_by(id=id_).one()
        except NoResultFound:
            abort(404, 'Item not found')

        return render_template('actor.html', actor=actor)
