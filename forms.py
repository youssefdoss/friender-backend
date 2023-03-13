from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from flask_wtf.file import FileRequired

class UserAddForm(FlaskForm):
    '''Form for adding users.'''

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    location = IntegerField('Location',validators=[DataRequired()])
    radius = IntegerField('radius', validators=[DataRequired()])

class UserUpdateForm(FlaskForm):
    '''Form for updating a user.'''

    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    location = IntegerField('Location',validators=[DataRequired(), NumberRange(min=10000, max=99999)])
    radius = IntegerField('radius', validators=[DataRequired()])
    bio = TextAreaField('bio')

class LoginForm(FlaskForm):
    '''Login form.'''

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class UploadImageForm(FlaskForm):
    '''Image upload form'''
    file = FileField('Image', [FileRequired()])