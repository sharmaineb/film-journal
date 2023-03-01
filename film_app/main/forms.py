from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from film_app.models import Genre, Film, List, Entry, User

class FilmForm(FlaskForm):
    """Form to create a film"""
    title = StringField('Film Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    watched_date = DateField('Date Watched or Will Watch:')
    list = QuerySelectField('List',
        query_factory=lambda: List.query, allow_blank=False)
    genre = SelectField('Genre', choices=Genre.choices())
    entries = QuerySelectMultipleField('Entries',
        query_factory=lambda: Entry.query)
    submit = SubmitField('Submit')

class ListForm(FlaskForm):
    """Form to create a list."""
    name = StringField('List Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField('List Description')
    submit = SubmitField('Submit')


class EntryForm(FlaskForm):
    """Form to create a entry."""
    name = StringField('Entry:',
        validators=[DataRequired(), Length(min=3, max=700)])
    submit = SubmitField('Submit')