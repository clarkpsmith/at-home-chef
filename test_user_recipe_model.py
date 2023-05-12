from app import app
import os
from unittest import TestCase

from models import db, User, Recipe, User_Favorite

os.environ['DATABASE_URL'] = "postgresql:///athomecheftest"

class UserRecipeModelTestCase(TestCase):
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

        new_recipe = Recipe(recipe_id = 2000,
        title = "Roast Chicken",
        image = "https://www.recipetineats.com/wp-content/uploads/2020/02/Honey-Garlic-Chicken-Breast_5-SQ.jpg")
        db.session.add(new_recipe)
        db.session.commit()

        self.user1 = User.query.get(user1_id)
  

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        db.drop_all()
        return res



    def test_recipe_model(self):
        """does recipe model work"""

        new_recipe = Recipe(recipe_id = 3000,
        title = "Roast Beef",
        image = "https://www.thespruceeats.com/thmb/tDWJzDYBuRqGuQIRuEr4yRMVGzQ=/2696x2696/smart/filters:no_upscale()/marinated-rump-roast-3058682-hero-01-0977a498722f47debaa7034c13053048.jpg"
)
        db.session.add(new_recipe)
        db.session.commit()

        recipe = Recipe.query.get(3000)
        self.assertEqual(recipe.recipe_id, 3000)
        self.assertEqual(recipe.title, "Roast Beef")
        self.assertEqual(recipe.image, "https://www.thespruceeats.com/thmb/tDWJzDYBuRqGuQIRuEr4yRMVGzQ=/2696x2696/smart/filters:no_upscale()/marinated-rump-roast-3058682-hero-01-0977a498722f47debaa7034c13053048.jpg")


    def test_user_recipe_model(self):
        """Does user_recipe model work"""

        new_favorite = User_Favorite(recipe_id = 2000, user_id = self.user1.id)
        new_favorite.id = 4000
        new_favorite_id = new_favorite.id
        db.session.add(new_favorite)
        db.session.commit()
        self.assertEqual(len(self.user1.recipes), 1)
        self.assertEqual(len(User_Favorite.query.all()), 1)
        favorite = User_Favorite.query.get(4000)
        self.assertEqual(favorite.user_id, self.user1.id)
        

      
    