"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from film_app.models import Film, List, Entry, User
from film_app.main.forms import FilmForm, ListForm, EntryForm

# Import app and db from film_app package so that we can run app
from film_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

# routes

@main.route('/')
def homepage():
    all_films = Film.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_films=all_films, all_users=all_users)

@main.route('/create_film', methods=['GET', 'POST'])
@login_required
def create_film():
    form = FilmForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_film = Film(
            title=form.title.data,
            release_date=form.release_date.data,
            list=form.list.data,
            genre=form.genre.data,
            entries=form.entries.data
        )
        db.session.add(new_film)
        db.session.commit()

        flash('New film was created successfully.')
        return redirect(url_for('main.film_detail', film_id=new_film.id))
    return render_template('create_film.html', form=form)

@main.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    form = ListForm()
    if form.validate_on_submit():
        new_list = List(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_list)
        db.session.commit()

        flash('New list created successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_list.html', form=form)

@main.route('/create_entry', methods=['GET', 'POST'])
@login_required
def create_entry():
    form = EntryForm()
    if form.validate_on_submit():
        new_entry = Entry(
            name=form.name.data
        )
        db.session.add(new_entry)
        db.session.commit()

        flash('New entry created successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_entry.html', form=form)

@main.route('/film/<film_id>', methods=['GET', 'POST'])
def film_detail(film_id):
    film = Film.query.get(film_id)
    form = FilmForm(obj=film)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        film.title = form.title.data
        film.release_date = form.release_date.data
        film.list = form.list.data
        film.genre = form.genre.data
        film.entries = form.entries.data

        db.session.commit()

        flash('Film was updated successfully.')
        return redirect(url_for('main.film_detail', film_id=film_id))

    return render_template('film_detail.html', film=film, form=form)

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)

@main.route('/favorite/<film_id>', methods=['POST'])
@login_required
def favorite_film(film_id):
    film = Film.query.get(film_id)
    if film in current_user.favorite_films:
        flash('Film already in favorites.')
    else:
        current_user.favorite_films.append(film)
        db.session.add(current_user)
        db.session.commit()
        flash('Film added to favorites.')
    return redirect(url_for('main.film_detail', film_id=film_id))

@main.route('/unfavorite/<film_id>', methods=['POST'])
@login_required
def unfavorite_film(film_id):
    film = Film.query.get(film_id)
    if film not in current_user.favorite_films:
        flash('Film not in favorites.')
    else:
        current_user.favorite_films.remove(film)
        db.session.add(current_user)
        db.session.commit()
        flash('Film removed from favorites.')
    return redirect(url_for('main.film_detail', film_id=film_id))

@main.route('/watchlist/<film_id>', methods=['POST'])
@login_required
def watch_film(film_id):
    film = Film.query.get(film_id)
    if film in current_user.watchlist_films:
        flash('Film already in watchlist.')
    else:
        current_user.watchlist_films.append(film)
        db.session.add(current_user)
        db.session.commit()
        flash('Film added to watchlist.')
    return redirect(url_for('main.film_detail', film_id=film_id))

@main.route('/unwatchlist/<film_id>', methods=['POST'])
@login_required
def unwatchlist_film(film_id):
    film = Film.query.get(film_id)
    if film not in current_user.watchlist_films:
        flash('Film not in watchlist')
    else:
        current_user.watchlist_films.remove(film)
        db.session.add(current_user)
        db.session.commit()
        flash('Film removed from watchlist.')
    return redirect(url_for('main.film_detail', film_id=film_id))