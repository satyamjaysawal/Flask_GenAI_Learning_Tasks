from flask import Flask, render_template, request, jsonify
from forms import FlightSearchForm
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

def load_flight_data():
    with open('flights.json') as f:
        return json.load(f)

@app.route('/')
def home():
    form = FlightSearchForm()  # Initializing form here
    return render_template('search.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
def search_flights():
    form = FlightSearchForm()
    results = []
    if form.validate_on_submit():
        data = load_flight_data()
        from_city = form.from_city.data
        to_city = form.to_city.data
        departure_date = form.departure_date.data
        return_date = form.return_date.data
        travel_class = form.travel_class.data
        special_fare = form.special_fare.data

        # Check if flight data matches search criteria
        if data['from'] == from_city and data['to'] == to_city:
            if departure_date and data['departure_date'] != str(departure_date):
                return render_template('search.html', form=form, results=results)
            if return_date and data['return_date'] != str(return_date):
                return render_template('search.html', form=form, results=results)
            if travel_class and travel_class in data['travel-class']:
                if special_fare:
                    fare_data = data['travel-class'][travel_class]['special_fare_option']
                    if special_fare in fare_data:
                        results.append({
                            'flight': data,
                            'special_fare_selected' : special_fare,
                            'fare': fare_data[special_fare],
                            'travel_class': travel_class
                        })
                else:
                    results.append(data)

    return render_template('search.html', form=form, results=results)

if __name__ == '__main__':
    app.run(debug=True)
