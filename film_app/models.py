# Create your models here.
from film_app.extensions import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)
    
class Genre(FormEnum):
    COMEDY = 'Comedy'
    DRAMA = 'Drama'
    ROMANCE = 'Romance'
    ACTION = 'Action'
    DOCUMENTARY = 'Documentary'
    HORROR = 'Horror'

class Film(db.Model):
    """Film Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    watched_date = db.Column(db.Date)
    director = db.Column(db.String(100), nullable=False)

    # the lists
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('List', back_populates='films')

    # the genres 
    genre = db.Column(db.Enum(Genre), default=Genre.COMEDY)

    # the entries
    entries = db.relationship(
        'Entry', secondary='film_entry', back_populates='films'
    )

    # who favorited this film?
    users_who_favorited = db.relationship(
        'User', secondary='user_film', back_populates='favorite_films'
    )

    # # who added film to watchlist?
    # users_who_want_to_watch = db.relationship(
    #     'User', secondary='user_film', back_populates='watchlist_films'
    # )

    def __str__(self):
        return f'<Film: {self.title}>'

    def __repr__(self):
        return f'<Film: {self.title}>'
    
class List(db.Model):
    """List model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500))
    films = db.relationship('Film', back_populates='list')

    def __str__(self):
        return f'<List: {self.name}>'

    def __repr__(self):
        return f'<List: {self.name}>'
    
class Entry(db.Model):
    """Entry model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    films = db.relationship(
        'Film', secondary='film_entry', back_populates='entries')

    def __str__(self):
        return f'<Entry: {self.name}>'

    def __repr__(self):
        return f'<Entry: {self.name}>'

film_entry_table = db.Table('film_entry',
    db.Column('film_id', db.Integer, db.ForeignKey('film.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_films = db.relationship(
        'Film', secondary='user_film', back_populates='users_who_favorited')

    def __repr__(self):
        return f'<User: {self.username}>'
    

favorite_films_table = db.Table('user_film',
    db.Column('film_id', db.Integer, db.ForeignKey('film.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# watchlist_films_table = db.Table('user_film',
#     db.Column('film_id', db.Integer, db.ForeignKey('film.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )



