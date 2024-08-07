# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, Optional

class FlightSearchForm(FlaskForm):
    from_city = StringField('From City', validators=[DataRequired()])
    to_city = StringField('To City', validators=[DataRequired()])
    departure_date = DateField('Departure Date', format='%Y-%m-%d', validators=[Optional()])
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[Optional()])
    travel_class = SelectField('Travel Class', choices=[('economy', 'Economy'), ('business', 'Business'), ('first_class', 'First Class')], validators=[Optional()])
    special_fare = SelectField('Special Fare', choices=[('Regular', 'Regular'), ('Student', 'Student'), ('Senior Citizen', 'Senior Citizen'), ('Armed Forces', 'Armed Forces'), ('Doctor and Nurses', 'Doctor and Nurses')], validators=[Optional()])
