from app import app
import os
from unittest import TestCase

from models import db, User, Recipe, User_Comment

os.environ['DATABASE_URL'] = "postgresql:///athomecheftest"

db.create_all()


class UserCommentModelTestCase(TestCase):
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



    def test_user_comment_model(self):
        """does recipe model work"""

        new_recipe = Recipe(recipe_id = 3000,
        title = "Roast Beef",
        image = "https://www.thespruceeats.com/thmb/tDWJzDYBuRqGuQIRuEr4yRMVGzQ=/2696x2696/smart/filters:no_upscale()/marinated-rump-roast-3058682-hero-01-0977a498722f47debaa7034c13053048.jpg"
)
        db.session.add(new_recipe)
        db.session.commit()

        comment = User_Comment(user_id =self.user1.id, recipe_id = 3000, comment = "This Roast Beef is Delicious")
        db.session.add(comment)
        db.session.commit()
        self.assertEqual(len(User_Comment.query.all()), 1)
        comment = User_Comment.query.get(1)
        self.assertEqual(comment.recipe_id, 3000)
        self.assertEqual(comment.comment, "This Roast Beef is Delicious")
        self.assertEqual(comment.user.username, "user1")
       


      
    