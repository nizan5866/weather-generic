import flask
from flask import Flask, request
import requests
import datetime
import os
from datetime import datetime as dt
from datetime import timedelta
#export FLASK_APP=hello.py (to remember to add this to bash for testing)
app = Flask(__name__)
WEATHER_KEY = os.environ.get("WEATHER_KEY")


@app.route("/")
def get_landing_page():
    return flask.send_file("website.html")


def __stringify_date(date: dt) -> str:
    return f"{date.year}-{date.month}-{date.day}"


def __fahrenheit_to_celsius(temp):
    # (F-32) * 5/9 = C (5/9 = 0.5555, 32*(5/7) = 17.777
    return 0.55*temp - 17.777


def __json_days_filtered(json_obj: dict) -> dict:
    res = {}
    days = json_obj["days"]
    for day in days:
        date = day["datetime"]
        sunrise = int(day["sunrise"][0:2]) #this is in the form "hh:mm:ss"
        sunset = int(day["sunset"][0:2])
        humidity = day["humidity"]
        day_hours = day["hours"]
        sum_day_degree = 0
        day_h_counter = 0 #hours counter
        sum_night_degree = 0
        night_h_counter = 0 
        for hour in day_hours:
            int_hour = int(hour["datetime"][0:2])
            if sunrise <= int_hour <= sunset:
                sum_day_degree += hour["temp"]
                day_h_counter += 1
            else:
                sum_night_degree += hour["temp"]
                night_h_counter += 1
        avr_day_degree = round(__fahrenheit_to_celsius(sum_day_degree/day_h_counter))
        avr_night_degree = round(__fahrenheit_to_celsius(sum_night_degree/night_h_counter))
        the_year, the_month, the_day = (int(x) for x in date.split("-"))
        # %A will return only the week day in the form of "sunday" etc
        day_of_the_week = datetime.date(the_year, the_month, the_day).strftime("%A")
        # using aaday because that's how it's decoded, by a-b order in js
        res[date] = {"aday": day_of_the_week, "avr_day": avr_day_degree, "avr_night": avr_night_degree, "humidity": humidity}
    return res


@app.post("/get_data")
def get_data():
    """this is the main function, sends get req to the weather api and response accordingly"""
    HTTP_OK :int = 200
    key = WEATHER_KEY
    city = request.get_json()["location"]
    tomorrow = dt.today() + timedelta(days=1)
    future_day = tomorrow + timedelta(days=6)
    today_str, fd_str = __stringify_date(tomorrow), __stringify_date(future_day)
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{today_str}/{fd_str}?unitGroup=us&key={key}&contentType=json"
    print(url)
    response = requests.get(url)
    if response.status_code != HTTP_OK:
        if response.status_code == 400:
            raise requests.exceptions.RequestException("Bad values for location")
        raise requests.exceptions.RequestException(f"Sorry. Something went wrong.")
    json_parsed = response.json()
    extra_location = {"fullLocation": json_parsed["resolvedAddress"]}
    full_data = flask.jsonify({"status": True, **extra_location, "relData": __json_days_filtered(json_parsed)})
    return full_data



@app.errorhandler(requests.exceptions.RequestException)
def requests_exception_handler(error):
    return flask.jsonify(status=False, message=str(error))


@app.errorhandler(Exception)
def exception_handler(error):
    app.logger.exception(error)
    return flask.jsonify(status=False, message=str(error))


@app.errorhandler(404)
def page_not_found(error):
    return flask.jsonify(status=False, message="page not found")


if __name__ == '__main__':
    app.run(host="0.0.0.0")