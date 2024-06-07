from flask import Flask, render_template, request
from flask_wtf import FlaskForm

from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField

# Define your form class
class InfoForm(FlaskForm):
    breed = StringField("What Breed are you?", validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    message = ''

    if form.validate_on_submit():
        breed = form.breed.data  # Access the submitted data
        message = f'You selected breed: {breed}'
        form.breed.data = ''  # Clear the field after submission

    return render_template('index.html', form=form, message=message)

if __name__ == '__main__':
    app.run(debug=True)
