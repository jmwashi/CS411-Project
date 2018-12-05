from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class MeetUpCreateForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    submit = SubmitField('Create MeetUp')

class EventCreateForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    time = StringField('time', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    submit = SubmitField('Create Event')
