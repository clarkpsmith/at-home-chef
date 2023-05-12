import random
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    first_name = db.Column(
        db.Text,
        nullable=False
        )
    last_name = db.Column(
    db.Text,
    nullable = False
    )
    password = db.Column(
        db.Text,
        nullable=False
    )

   
    recipes = db.relationship(
        'Recipe',
        secondary="users_favorites"
    )

    comments = db.relationship("User_Comment", backref="user", cascade="all, delete-orphan")
    

    @classmethod
    def signup(cls, username, first_name, last_name, email, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
        username=username,
        first_name = first_name,
        last_name = last_name,
        email=email,
        password=hashed_pwd,)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """find user with username and password.
        searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

            return False
            

class User_Favorite(db.Model):
    """users favorites table"""

    __tablename__ = 'users_favorites'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.recipe_id', ondelete='cascade'),
   
    )

class User_Comment(db.Model):
    """users comments table"""

    __tablename__ = "users_comments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now()
    )

    recipe_id = db.Column(
        db.Integer,
        db.ForeignKey('recipes.recipe_id', ondelete='cascade'),
    )

    comment = db.Column(db.Text, nullable = False)


class Recipe(db.Model):
    "liked recipe info"

    __tablename__= "recipes"

    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
    db.Text,
    nullable=False)
        
    image = db.Column(db.Text,
    nullable=False)



       
def connect_db(app):
        """Connect this database to Flask app"""

        db.app = app
        db.init_app(app)



def season():
    """set the season based on date"""

    currentMonth = datetime.now().month
    currentDay = datetime.now().day
    if currentMonth in [12,1,2]:
        season = "winter"
        if currentMonth == 12 and (currentDay > 10 and currentDay < 27):
            season = random.choice(["christmas","christmas","christmas","christmas","hanukkah", "christmas"])        
    if currentMonth in [3,4,5]:
        season = "spring"
    if currentMonth in [6,7,8]:
        season = "summer"
    if currentMonth in [9,10,11]:
        season = random.choice(["fall","autumn","fall"]) 
        if currentMonth == 11 and (currentDay > 21 and currentDay < 29):
            season ="thanksgiving"

    if season  in ["winter","christmas", "hanukkah"]:
        icon = "snowflake"
    elif season in "spring":
        icon = "tulip"
    elif season  in "summer":
        icon = "umbrella"
    elif season  in ["fall", "autumn"]:
        icon = "maple_leaf"
    elif season in "thanksgiving":
        icon = "turkey"
    return [season, icon]

    