

from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, User, Recipe, User_Favorite, User_Comment

os.environ['DATABASE_URL'] = "postgresql:///athomecheftest"

app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """test user views"""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        user1 = User.signup(
            username="user1", 
            first_name = "first1",
            last_name = "last1",
            email="clark.smith79@gmail.com", password="password")
        user1.id = 1000
        user1_id = user1.id
    
        db.session.commit()

        self.user1 = User.query.get(user1_id)


        new_recipe = Recipe(recipe_id = 2000,
        title = "Roast Chicken",
        image = "https://www.recipetineats.com/wp-content/uploads/2020/02/Honey-Garlic-Chicken-Breast_5-SQ.jpg")
        db.session.add(new_recipe)
        db.session.commit()
        self.user1.recipes.append(new_recipe)
        db.session.commit()


    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        db.drop_all()
        return res


    def test_detail(self):
        """test details page"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.get("/user")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Favorites", html)
            self.assertIn("first1 last1", html)
            self.assertIn("Roast Chicken", html)


    def test_show_edit_profile(self):
        """show edit profile"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.get("/user/editprofile")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Edit User", html)
            self.assertIn("Edit Your Profile", html)
            self.assertIn("Username", html)
            

    def test_update_profile(self):
        """test show update profile page"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.post("/user/editprofile", follow_redirects=True, data={
                              "username": "user2", "first_name":"first2", "last_name": "last2", "email": "user2@gmail.com", "password": "password" })
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("first2 last2", html)
            self.assertIn("user2", html)



    def test_warning_delete_user(self):
        """test warning to delete profile """

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.get('/user/deleteprofile')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Are you sure you want to delete your profile?", html)
            
            
           

    def test_delete_user(self):
        """test delete profile """

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.post('/user/deleteprofile', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            user = User.query.get(self.user1.id)
            self.assertFalse(user)

    
    def test_favorite_dish(self):
        """test favoriting a dish"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res1 = client.get("/dish/654959")
            html1 = res1.get_data(as_text=True)
            self.assertEqual(res1.status_code, 200)
            self.assertIn("not-favorited-btn", html1)
            res2 = client.post("/favorite/654959")
            self.assertEqual(res2.json["message"],"Dish Favorited")
            self.assertEqual(len(User_Favorite.query.all()), 2)
            res3 = client.get("/dish/654959")
            self.assertEqual(res3.status_code, 200)
            html3 = res3.get_data(as_text=True)
            self.assertIn("favorited-btn", html3)
           


    def test_remove_favorite_dish(self):
        """test remove favorite for a dish"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

         # set up favorite
        client.post("/favorite/654959")
        res1 = client.get("/dish/654959")
        html1 = res1.get_data(as_text=True)
        self.assertEqual(res1.status_code, 200)
        self.assertIn("favorited-btn", html1)
        res2 = client.post("/removefavorite/654959")
        self.assertEqual(res2.json["message"],"Removed Favorite")
        self.assertEqual(len(User_Favorite.query.all()), 1)
        res3 = client.get("/dish/654959")
        self.assertEqual(res3.status_code, 200)
        html3 = res3.get_data(as_text=True)
        self.assertIn("not-favorited-btn", html3)

    def test_favorite_dish_homepage(self):
        """test favoriting a dish from homepage"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

        res1 = client.post("/", data = {"dish": "pasta", "diet": "None"})
        html1 = res1.get_data(as_text=True)
        self.assertEqual(res1.status_code, 200)
        self.assertIn("not-favorited-btn", html1)
        res2 = client.post("/favorite/654959")
        self.assertEqual(res2.json["message"],"Dish Favorited")
        self.assertEqual(len(User_Favorite.query.all()), 2)
        res3 = client.post("/", data = {"dish": "pasta", "diet": "None"})
        self.assertEqual(res3.status_code, 200)
        html3 = res3.get_data(as_text=True)
        self.assertIn("favorited-btn", html3)        

    def test_remove_favorite_dish_homepage(self):
        """test remove favoriting a dish from homepage"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

        # set up favorite
        client.post("/favorite/654959")
        res1 = client.post("/", data = {"dish": "pasta", "diet": "None"})
        html1 = res1.get_data(as_text=True)
        self.assertEqual(res1.status_code, 200)
        self.assertIn("favorited-btn", html1)
        res2 = client.post("/removefavorite/654959")
        self.assertEqual(res2.json["message"],"Removed Favorite")
        self.assertEqual(len(User_Favorite.query.all()), 1)
        res3 = client.post("/", data = {"dish": "pasta", "diet": "None"})
        self.assertEqual(res3.status_code, 200)
        html3 = res3.get_data(as_text=True)
        self.assertIn("not-favorited-btn", html3)
            

    def test_remove_favorite_dish_detail_page(self):
        """test remove favoriting a dish fromd details page"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id

        # set up favorite
        client.post("/favorite/654959")
        res1 = client.get("/user")
        self.assertEqual(len(User_Favorite.query.all()), 2)
        html1 = res1.get_data(as_text=True)
        self.assertEqual(res1.status_code, 200)
        self.assertIn("Pasta With Tuna", html1)
        res2 = client.post("/removefavorite/654959")
        self.assertEqual(res2.json["message"],"Removed Favorite")
        self.assertEqual(len(User_Favorite.query.all()), 1)
        res3 = client.get("/user")
        self.assertEqual(res3.status_code, 200)
        html3 = res3.get_data(as_text=True)
        self.assertIn("Roast Chicken", html3)
            

    def test_send_grocery_list(self):
        """ test sending grocery list email to user"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.post("/dish/654959/grocerylist", follow_redirects=True)
            html = res.get_data(as_text=True)
            print(res)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Pasta With Tuna", html)      
            self.assertIn("Grocery list has been sent to your email address!", html)

    def test_add_comment(self):
        """test adding a user comment to a dish"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            self.assertEqual(len(User_Comment.query.all()), 0)
            res = client.post("/dish/654959/comment", data={"comment": "This Dish is Super!!"},follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(User_Comment.query.all()), 1)
            self.assertIn("This Dish is Super!!", html)


    def test_delete_comment(self):
        """test adding a user comment to a dish"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user1.id
            res = client.post("/dish/654959/comment", data={"comment": "This Dish is Super!!"},follow_redirects=True)
            self.assertEqual(len(User_Comment.query.all()), 1)
            res = client.post("/comment/1/delete")
            self.assertEqual(len(User_Comment.query.all()), 0)
            user = User_Comment.query.get(1)
            self.assertFalse(user)
