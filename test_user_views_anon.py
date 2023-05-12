from app import app
from unittest import TestCase

from models import db

app.config['WTF_CSRF_ENABLED'] = False

class AnonViewsTestCase(TestCase):
    """Test anonoymous views"""

    def test_signup(self):
        """test show signup page"""

        with app.test_client() as client:
            res = client.get("/signup")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Sign me up!", html)

    def test_login(self):
        """test show login page"""

        with app.test_client() as client:
            res = client.get("/login")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Welcome back!", html)


    def test_homepage(self):
        """test show homepage"""

        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Search", html)

    def test_search_dish(self):
        """test search for a dish"""

        with app.test_client() as client:
            res = client.post("/", data = {"dish": "pasta", "diet": "Vegan"})
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Simple Garlic Pasta", html)
            self.assertIn("Get this recipe!", html)
        
    def test_seasonal(self):
        """test seasonal page"""

        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["season"] = "fall"
            res = client.get("/seasonal")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Seasonal Dishes", html)
            self.assertIn("Get this recipe!", html)

    def test_show_dish(self):
        """test show dish"""

        with app.test_client() as client:
            res = client.get("/dish/654959")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Pasta With Tuna", html)
            self.assertIn("2 tablespoons Flour", html)
            self.assertIn("Cook pasta in a large pot of boiling water until al dente.", html)
            
    def test_unauthorized_details(self):
        """test unauthorized details request"""

        with app.test_client() as client:
            res = client.get("/user", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Access Denied Please Login First", html)
            

    def test_unauthorized_editprofile(self):
        """test unauthorized edit profile requesr"""

        with app.test_client() as client:
            res = client.get("/user/editprofile", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Access Denied Please Login First", html)
            

    def test_unauthorized_deleteprofile(self):
        """test unauthorized delete profile request"""

        with app.test_client() as client:
            res = client.get("/user/deleteprofile", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Access Denied Please Login First", html)


    def test_unauthorized_remove_favorite(self):
        """ test unauthorized remove favorite"""

        with app.test_client() as client:
            res = client.post("/removefavorite/1", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Access Denied Please Login First", html)


    def test_unauthorized_favorite(self):
        """ test unauthorized favorite"""

        with app.test_client() as client:
            res = client.post("/favorite/1", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Access Denied Please Login First", html)

    def test_unauthorized_get_grocery_list(self):
        """ test unauthorized get grocery list"""

        with app.test_client() as client:
            res= client.post("/dish/1/grocerylist", follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Access Denied Please Login First", html)
