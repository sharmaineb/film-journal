# # Create your tests here.
# import os
# from unittest import TestCase

# from datetime import date

# from film_app.extensions import app, db, bcrypt
# from film_app.models import Film, List, User, Genre

# """
# Run these tests with the command:
# python -m unittest film_app.main.tests
# """

# #################################################
# # Setup
# #################################################

# def create_films():
#     a1 = List(name='Greta Gerwig')
#     b1 = Film(
#         title='Lady Bird',
#         watched_date=date(2017, 11, 10),
#         list=a1
#     )
#     db.session.add(b1)

#     a2 = List(name='Tony Scott')
#     b2 = Film(title='True Romance', list=a2)
#     db.session.add(b2)
#     db.session.commit()

# def create_user():
#     password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
#     user = User(username='me1', password=password_hash)
#     db.session.add(user)
#     db.session.commit()

# #################################################
# # Tests
# #################################################

# class AuthTests(TestCase):
#     """Tests for authentication (login & signup)."""
 
#     def setUp(self):
#         """Executed prior to each test."""
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['DEBUG'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#         self.app = app.test_client()
#         db.drop_all()
#         db.create_all()

#     def test_signup(self):
#         # TODO: Write a test for the signup route. It should:
#         # - Make a POST request to /signup, sending a username & password
#         # - Check that the user now exists in the database
#         post_data = {
#             'username': 'sharshar',
#             'password': 'password123',
#         }

#         self.app.post('/signup', data=post_data)
#         response = self.app.get('/profile/sharshar')
#         response_text = response.get_data(as_text=True)
#         self.assertIn('sharshar', response_text)

#     def test_signup_existing_user(self):
#         # TODO: Write a test for the signup route. It should:
#         # - Create a user
#         # - Make a POST request to /signup, sending the same username & password
#         # - Check that the form is displayed again with an error message
#         create_user()
#         post_data = {
#             'username': 'me1',
#             'password': 'password',
#         }

#         response = self.app.post('/signup', data=post_data)
#         response_text = response.get_data(as_text=True)
#         self.assertIn('Sorry, username is already taken. Please try again.', response_text)

#     def test_login_correct_password(self):
#         # TODO: Write a test for the login route. It should:
#         # - Create a user
#         # - Make a POST request to /login, sending the created username & password
#         # - Check that the "login" button is not displayed on the homepage
#         create_user()
#         post_data = {
#             'username': 'me1',
#             'password': 'password',
#         }

#         self.app.post('/login', data=post_data)
#         response = self.app.get('/')
#         response_text = response.get_data(as_text=True)

#         self.assertNotIn('login', response_text)

#     def test_login_nonexistent_user(self):
#         # TODO: Write a test for the login route. It should:
#         # - Make a POST request to /login, sending a username & password
#         # - Check that the login form is displayed again, with an appropriate
#         #   error message
#         post_data = {
#             'username': 'charmander',
#             'password': 'password321',
#         }

#         response = self.app.post('/login', data=post_data)
#         response_text = response.get_data(as_text=True)
#         self.assertIn('User Not Found', response_text)

#     def test_login_incorrect_password(self):
#         # TODO: Write a test for the login route. It should:
#         # - Create a user
#         # - Make a POST request to /login, sending the created username &
#         #   an incorrect password
#         # - Check that the login form is displayed again, with an appropriate
#         #   error message
#         create_user()
#         post_data = {
#             'username': 'me1',
#             'password': 'incorrect',
#         }

#         response = self.app.post('/login', data=post_data)
#         response_text = response.get_data(as_text=True)

#         self.assertIn('Incorrect Password. Try Again.', response_text)

#     def test_logout(self):
#         # TODO: Write a test for the logout route. It should:
#         # - Create a user
#         # - Log the user in (make a POST request to /login)
#         # - Make a GET request to /logout
#         # - Check that the "login" button appears on the homepage
#         create_user()
#         post_data = {
#             'username': 'me1',
#             'password': 'password',
#         }

#         self.app.post('/login', data=post_data)
#         self.app.get('/logout')
#         response = self.app.get('/')
#         response_text = response.get_data(as_text=True)
#         self.assertIn('login', response_text)
