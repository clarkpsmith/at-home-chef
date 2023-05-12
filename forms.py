from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[InputRequired(message="Username Required")])
    first_name = StringField("First Name", validators=[InputRequired(message="First Name Required")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Last Name Required")])
    email = StringField('E-mail', validators=[InputRequired(), Email(message="Email Adress Not Valid")])
    password = PasswordField('Password', validators=[Length(min=6)])
   


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


# class EditProfile(FlaskForm):
#     """edit profile form"""

#     username = StringField('Username', validators=[DataRequired()])
#     first_name = 
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[Length(min=6)])
