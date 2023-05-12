from app import app
import os
from unittest import TestCase

from models import db, User
from sqlalchemy import exc

os.environ['DATABASE_URL'] = "postgresql:///athomecheftest"

class UserModelTestCase(TestCase):
    """Test user model."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        user1 = User.signup(
            username="user1", 
            first_name = "first1",
            last_name = "last1",
            email="user1@gmail.com", password="password")
        user1.id = 1000
        user1_id = user1.id
    
        db.session.commit()

        self.user1 = User.query.get(user1_id)
      

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        db.drop_all()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            first_name= "testfirst",
            last_name="testlast",
            password="HASHED_PASSWORD"
        )
        u.id = 3000
        u_id = u.id
        db.session.add(u)
        db.session.commit()
        user = User.query.get(u_id)

        self.assertEqual(len(user.recipes), 0)
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.first_name, "testfirst")
        self.assertEqual(user.username, "testuser")

    def test_valid_signup(self):
        """test valid signup"""

        user_test = User.signup(
            "user_test", "testfirst", "testlast", "user_test@gmail.com", "password" )
        user_test.id = 3000
        user_test_id = user_test.id
        db.session.commit()
        test_user = User.query.get(user_test_id)
        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.username, "user_test")
        self.assertEqual(test_user.first_name, "testfirst")
        self.assertEqual(test_user.last_name, "testlast")
        self.assertEqual(test_user.email, "user_test@gmail.com")
        self.assertNotEqual(test_user.password, "password")
        self.assertTrue(test_user.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        """test that using an existing username on signup raises an error"""

        user_test = User.signup(
            "user1", "testfirst", "testlast", "user_test@gmail.com", "password")
        user_test.id = 4000
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        """test no email address input raises error"""

        user_test = User.signup(
            "user3","testfirst", "testlast", None, "password" )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_first_name_signup(self):
        """test invalid first name on signup"""

        user_test = User.signup(
            "user3","user_test@gmail.com", None, "testlast", "password" )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_last_name_signup(self):
        """test invalid last name on signup"""

        user_test = User.signup(
            "user3","user_test@gmail.com", "testfirst", None, "password" )

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password(self):
        """test invalid password"""

        with self.assertRaises(ValueError) as context:
            user_test = User.signup(
                "user3", "testfirst", "testlast", "user_test@gmail.com", "")

        with self.assertRaises(ValueError) as context:
            user_test = User.signup(
                "user3",  "testfirst", "testlast", "user_test@gmail.com", None)

    def test_valid_authentication(self):
        """test login method"""

        good_username = User.authenticate("user1", "password")
        self.assertEqual(self.user1, good_username)

    def test_invalid_password(self):
        self.assertFalse(User.authenticate("user1", "piggies"))

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("user7", "password"))
