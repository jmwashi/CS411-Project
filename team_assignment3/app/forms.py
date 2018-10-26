from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    city = StringField('Location', validators=[DataRequired()])
    numberOfRestaruants = IntegerField('Number of Searches', validators=[DataRequired()])
    submit = SubmitField('Search')
