import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler_test_message"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all() 
        
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        u1 = User(
            email = 'test@gmail.com',
            username = 'testuser',
            password = 'password'
        )
        db.session.add(u1)
        db.session.commit()

        m1 = Message(
            text = 'This is a test.',
            user_id = u1.id
        )        
        db.session.add(m1)
        db.session.commit()
        self.assertEqual(len(u1.messages), 1)
        self.assertEqual(m1.user.email, 'test@gmail.com')
        self.assertEqual(m1.user.username, 'testuser')
        self.assertEqual(m1.user.password, 'password')
        self.assertEqual(m1.text, 'This is a test.')
        self.assertEqual(m1.user_id, u1.id)
        
        m2 = Message(
            text = 'This is the second message',
            user_id = u1.id
        ) 
        db.session.add(m2)
        db.session.commit()
        self.assertEqual(len(u1.messages), 2)
