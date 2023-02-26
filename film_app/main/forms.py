# Create your forms here.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from film_app.models import Genre, Film, Director, Entry, User

class FilmForm(FlaskForm):
    """Form to create a film"""
    title = StringField('Film Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    release_date = DateField('Date Released')
    director = QuerySelectField('Director',
        query_factory=lambda: Director.query, allow_blank=False)
    genre = SelectField('Genre', choices=Genre.choices())
    entries = QuerySelectMultipleField('Entries',
        query_factory=lambda: Entry.query)
    submit = SubmitField('Submit')

class DirectorForm(FlaskForm):
    """Form to create a director."""
    name = StringField('Director Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    biography = TextAreaField('Director Biography')
    submit = SubmitField('Submit')


class EntryForm(FlaskForm):
    """Form to create a entry."""
    name = StringField('Entry Name',
        validators=[DataRequired(), Length(min=3, max=200)])
    submit = SubmitField('Submit')