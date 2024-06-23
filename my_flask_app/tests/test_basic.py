import unittest
from app import create_app, db
from app.models import User

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_register_and_login(self):
        # Register a new user
        response = self.client.post('/register', data=dict(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)

        # Log in with the new user
        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Home Page', response.data)

        # Log out
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data)

if __name__ == '__main__':
    unittest.main()
