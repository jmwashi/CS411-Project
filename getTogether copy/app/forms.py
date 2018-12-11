from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,RadioField,IntegerField
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

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    city = StringField('Location', validators=[DataRequired()])
    numberOfRestaruants = IntegerField('Number of Searches', validators=[DataRequired()])
    submit = SubmitField('Search')

class SelectForm(FlaskForm):
    selection = RadioField('Label',choices=[('value','description'),('value_two','whatever')])
    submit = SubmitField('Submit')

class SearchEventForm(FlaskForm):
	keyword = StringField('Keyword', validators=[DataRequired()])
	sort_by = RadioField("Sort_by",choices=[("date","date"),("distance","distance"),("best","best")],validators=[DataRequired()])
	location = StringField("Location",validators=[DataRequired()])
	location_within = IntegerField ("Location_within_km",validators=[DataRequired()])
	price = RadioField("price",choices=[("free","free"),("paid","paid")],validators=[DataRequired()])
	start_after = StringField("Start_after (YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
	start_before = StringField("Start_before (YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
	submit = SubmitField('Search')

class EBForm(FlaskForm):
    selection = RadioField('Label',choices=[('value','description'),('value_two','whatever')])
    submit = SubmitField('Submit')

class GuestForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add')