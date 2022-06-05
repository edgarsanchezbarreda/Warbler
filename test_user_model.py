"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None)

        u2 = User.signup("test2", "email2@email.com", "password", None)

        db.session.commit()

        u1 = User.query.get(u1.id)
        u2 = User.query.get(u2.id)

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test2.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.__repr__(), f"<User #{u.id}: testuser, test@test.com>")
        

    
    def test_user_is_following_model(self):

        self.u1.following.append(self.u2)        
        db.session.commit()
        self.assertTrue(self.u1.is_following(self.u2)) 

        self.u1.following = []
        db.session.commit()
        self.assertFalse(self.u1.is_following(self.u2))


    def test_user_is_followed_by_model(self):

        self.u2.following.append(self.u1)        
        db.session.commit()
        self.assertTrue(self.u1.is_followed_by(self.u2)) 

        self.u2.following = []
        db.session.commit()
        self.assertFalse(self.u1.is_followed_by(self.u2))
           
    def test_user_signup_model(self):
        u3 = User.signup("test3", "email3@email.com", "password", None)
        db.session.commit()

        self.assertIsInstance(u3, User)

        u4 = User.signup(None, "email4@email.com", "password4", None)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
        

    def test_user_authenticate_model(self):
        self.assertEqual(self.u1.authenticate('test1', 'password'), self.u1)
        self.assertNotEqual(self.u1.authenticate('test1', 'wrongpassword'), self.u1)
        self.assertNotEqual(self.u1.authenticate('wrongusername', 'password'), self.u1)