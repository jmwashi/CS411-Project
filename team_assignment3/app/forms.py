from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField ,RadioField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    city = StringField('Location', validators=[DataRequired()])
    numberOfRestaruants = IntegerField('Number of Searches', validators=[DataRequired()])
    submit = SubmitField('Search')

class SearchEventForm(FlaskForm):
	keyword = StringField('Keyword', validators=[DataRequired()])
	sort_by = RadioField("Sort_by",choices=[("date","date"),("distance","distance"),("best","best")],validators=[DataRequired()])
	location = StringField("Location",validators=[DataRequired()])
	location_within = IntegerField ("Location_within_km",validators=[DataRequired()])
	price = RadioField("price",choices=[("free","free"),("paid","paid")],validators=[DataRequired()])
	start_after = StringField("Start_after (YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
	start_before = StringField("Start_before (YYYY-MM-DD HH:MM:SS)", validators=[DataRequired()])
	submit = SubmitField('Search')