# import os
# import unittest
# import app

# from datetime import date
# from film_app.extensions import app, db, bcrypt
# from film_app.models import Film, Director, User, Genre, Entry

# """
# Run these tests with the command:
# python -m unittest film_app.main.tests
# """

# #################################################
# # Setup
# #################################################

# def login(client, username, password):
#     return client.post('/login', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)

# def logout(client):
#     return client.get('/logout', follow_redirects=True)

# def create_films():
#     a1 = Director(name='Greta Gerwig')
#     b1 = Film(
#         title='Lady Bird',
#         release_date=date(2017, 11, 10),
#         director=a1
#     )
#     db.session.add(b1)

#     a2 = Director(name='Tony Scott')
#     b2 = Film(title='True Romance', director=a2)
#     db.session.add(b2)
#     db.session.commit()

# def create_user():
#     # Creates a user with username 'me1' and password of 'password'
#     password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
#     user = User(username='me1', password=password_hash)
#     db.session.add(user)
#     db.session.commit()

# #################################################
# # Tests
# #################################################

# class MainTests(unittest.TestCase):
 
#     def setUp(self):
#         """Executed prior to each test."""
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         self.app = app.test_client()
#         db.drop_all()
#         db.create_all()
 
#     def test_homepage_logged_out(self):
#         """Test that the films show up on the homepage."""
#         # Set up
#         create_films()
#         create_user()

#         # Make a GET request
#         response = self.app.get('/', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#         # Check that page contains all of the things we expect
#         response_text = response.get_data(as_text=True)
#         self.assertIn('Lady Bird', response_text)
#         self.assertIn('True Romance', response_text)
#         self.assertIn('me1', response_text)
#         self.assertIn('Log In', response_text)
#         self.assertIn('Sign Up', response_text)

#         # Check that the page doesn't contain things we don't expect
#         # (these should be shown only to logged in users)
#         self.assertNotIn('Create Film', response_text)
#         self.assertNotIn('Create Director', response_text)
#         self.assertNotIn('Create Entry', response_text)
 
#     def test_homepage_logged_in(self):
#         """Test that the films show up on the homepage."""
#         # Set up
#         create_films()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make a GET request
#         response = self.app.get('/', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)

#         # Check that page contains all of the things we expect
#         response_text = response.get_data(as_text=True)
#         self.assertIn('Lady Bird', response_text)
#         self.assertIn('True Romance', response_text)
#         self.assertIn('me1', response_text)
#         self.assertIn('Create Film', response_text)
#         self.assertIn('Create Director', response_text)
#         self.assertIn('Create Entry', response_text)

#         # Check that the page doesn't contain things we don't expect
#         # (these should be shown only to logged out users)
#         self.assertNotIn('Log In', response_text)
#         self.assertNotIn('Sign Up', response_text)

#     def test_film_detail_logged_out(self):
#         """Test that the film appears on its detail page."""
#         # TODO: Use helper functions to create films, director, user
#         create_films()
#         create_user()

#         # TODO: Make a GET request to the URL /film/1, check to see that the
#         # status code is 200
#         response = self.app.get('/film/1', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)


#         # TODO: Check that the response contains the film's title, publish date,
#         # and director's name
#         response_text = response.get_data(as_text=True)
#         self.assertIn("<h1>Lady Bird</h1>", response_text)
#         self.assertIn("Greta Gerwig", response_text)

#         # TODO: Check that the response does NOT contain the 'Favorite' button
#         # (it should only be shown to logged in users)
#         self.assertNotIn("Favorite This Film", response_text)

#     def test_film_detail_logged_in(self):
#         """Test that the film appears on its detail page."""
#         # TODO: Use helper functions to create films, directors, user, & to log in
#         create_films()
#         create_user()
#         login(self.app, 'me1', 'password')
#         # TODO: Make a GET request to the URL /film/1, check to see that the
#         # status code is 200
#         response = self.app.get('/film/1', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         # TODO: Check that the response contains the film's title, publish date,
#         # and director's name
#         response_text = response.get_data(as_text=True)
#         self.assertIn("<h1>Lady Bird</h1>", response_text)
#         self.assertIn("Greta Gerwig", response_text)
#         # TODO: Check that the response contains the 'Favorite' button
#         self.assertIn("Favorite This Film", response_text)

#     def test_update_film(self):
#         """Test updating a film."""
#         # Set up
#         create_films()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make POST request with data
#         post_data = {
#             'title': 'Little Women',
#             'release_date': '2012-12-25',
#             'director': 1,
#             'genre': 'Comedy',
#             'entries': []
#         }
#         self.app.post('/film/1', data=post_data)
        
#         # Make sure the film was updated as we'd expect
#         film = Film.query.get(1)
#         self.assertEqual(film.title, 'Little Women')
#         self.assertEqual(film.release_date, date(2019, 12, 25))
#         self.assertEqual(film.genre, Genre.DRAMA)

#     def test_create_film(self):
#         """Test creating a film."""
#         # Set up
#         create_films()
#         create_user()
#         login(self.app, 'me1', 'password')

#         # Make POST request with data
#         post_data = {
#             'title': 'Frances Ha',
#             'release_date': '2013-05-17',
#             'director': 1,
#             'genre': 'ROMANCE',
#             'genres': []
#         }
#         self.app.post('/create_film', data=post_data)

#         # Make sure film was updated as we'd expect
#         created_film = Film.query.filter_by(title='Frances Ha').one()
#         self.assertIsNotNone(created_film)
#         self.assertEqual(created_film.list.name, 'Greta Gerwig')

#     def test_create_film_logged_out(self):
#         """
#         Test that the user is redirected when trying to access the create film 
#         route if not logged in.
#         """
#         # Set up
#         create_films()
#         create_user()

#         # Make GET request
#         response = self.app.get('/create_film')

#         # Make sure that the user was redirecte to the login page
#         self.assertEqual(response.status_code, 302)
#         self.assertIn('/login?next=%2Fcreate_film', response.location)

#     def test_create_director(self):
#         """Test creating an director."""
#         # TODO: Create a user & login (so that the user can access the route)
#         create_user()
#         login(self.app, 'me1', 'password')
#         # TODO: Make a POST request to the /create_director route
#         post_data = {
#             'name': 'Damien Chazelle',
#             'biography': 'Directed: Whiplash, La La Land.'
#         }

#         self.app.post('/create_director', data=post_data)
#         # TODO: Verify that the director was updated in the database
#         create_director = Director.query.filter_by(name='Damien Chazelle').one()
#         self.assertIsNotNone(create_director)
#         self.assertEqual(create_director.biography, 'Directed: Whiplash, La La Land, and Babylon.')

#     def test_create_entry(self):
#         # TODO: Create a user & login (so that the user can access the route)
#         create_user()
#         login(self.app, 'me1', 'password')
#         # TODO: Make a POST request to the /create_genre route, 
#         post_data = {
#             'name': 'Test Entry',
#         }
#         self.app.post('/create_entry', data=post_data)
#         # TODO: Verify that the genre was updated in the database
#         create_entry = Entry.query.filter_by(name='Test Entry').one()
#         self.assertIsNotNone(create_entry)
#         self.assertEqual(create_entry.name, 'Test Entry')

#     def test_profile_page(self):
#         # TODO: Make a GET request to the /profile/me1 route
#         create_user()
#         login(self.app, 'me1', 'password')
#         # TODO: Verify that the response shows the appropriate user info
#         response = self.app.get('/profile/me1')
#         self.assertEqual(response.status_code, 200)

#         response_text = response.get_data(as_text=True)
#         self.assertIn('me1', response_text)

#     def test_favorite_film(self):
#         # TODO: Login as the user me1
#         create_user()
#         create_films()
#         login(self.app, 'me1', 'password')
#         # TODO: Make a POST request to the /favorite/1 route
#         post_data = {
#             'film_id': 1
#         }

#         response = self.app.post('/favorite/1', data=post_data)
#         # TODO: Verify that the film with id 1 was added to the user's favorites
#         user = User.query.filter_by(username='me1').one()
#         film = Film.query.get(1)
#         self.assertIn(film, user.favorite_films)

#     def test_unfavorite_film(self):
#         # TODO: Login as the user me1, and add film with id 1 to me1's favorites
#         create_films()
#         create_user()
#         login(self.app, 'me1', 'password')
#         # TODO: Make a POST request to the /unfavorite/1 route
#         post_data = {
#             'film,_id': 1
#         }

#         response = self.app.post('/unfavorite/1', data=post_data)
#         # TODO: Verify that the film with id 1 was removed from the user's 
#         # favorites
#         user = User.query.filter_by(username='me1').one()
#         film = Film.query.get(1)
#         self.assertNotIn(film, user.favorite_films)
