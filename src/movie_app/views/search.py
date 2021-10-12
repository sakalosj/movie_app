from flask import render_template, request
from flask.views import MethodView
from wtforms import Form, StringField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import CheckboxInput, ListWidget

from db.actor import ActorModel
from db.movie import MovieModel

search_choices = {'movies': 'Movies', 'actor_first_name': 'Actor first name',
                  'actor_last_name': 'Actor last name'}


class SearchForm(Form):
    search = StringField('search', [DataRequired()])
    search_in = SelectMultipleField('Search in',
                                    choices=[(k, v) for k, v in search_choices.items()], option_widget=CheckboxInput(),
                                    widget=ListWidget(prefix_label=True))


class SearchView(MethodView):
    def get(self):
        form = SearchForm()
        form.search_in.data = search_choices.keys()
        return render_template('search.html', form=form)


    def post(self):
        form = SearchForm(request.form)
        actors, movies = None, None
        if form.validate():

            if 'movies' in form.search_in.data:
                movies = MovieModel.search_by_title(form.search.data)
            if {'actor_first_name', 'actor_last_name'}.issubset(set(form.search_in.data)):
                actors = ActorModel.search_by(form.search.data, [ActorModel.first_name, ActorModel.last_name])
            elif 'actor_first_name' in form.search_in.data:
                actors = ActorModel.search_by(form.search.data, [ActorModel.first_name])
            elif 'actor_last_name' in form.search_in.data:
                actors = ActorModel.search_by(form.search.data, [ActorModel.last_name])

            return render_template('search.html', form=form, movies=movies, actors=actors)
        return render_template('search.html', form=form)
