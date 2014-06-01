import urllib2
import json

api_call = 'http://api.wunderground.com/api/f01e373f0b1f215e/geolookup/{0}/q/{1}/{2}.json'
metric = True


# Perform an API call and get the JSON data.
def query(feature, country, city):
    f = urllib2.urlopen(api_call.format(feature, country, city))
    json_string = f.read()
    f.close()
    return json.loads(json_string)


# Get the current conditions.
def weather_current(country, city):
    parsed_json = query('conditions', country, city)

    location = parsed_json['current_observation']['display_location']['full']
    condition = parsed_json['current_observation']['weather']
    temp = str(parsed_json['current_observation']['temp_c' if metric else 'temp_f']) + ' C' if metric else ' F'
    windchill = str(
        parsed_json['current_observation']['windchill_c' if metric else 'windchill_f']) + ' C' if metric else ' F'
    feelslike = str(
        parsed_json['current_observation']['feelslike_c' if metric else 'feelslike_f']) + ' C' if metric else ' F'

    if not 'NA' in windchill:
        return "It is currently %s and %s (windchill: %s) in %s." % (condition.lower(), temp, windchill, location)
    else:
        return "It is currently %s and %s (feels like %s) in %s." % (condition.lower(), temp, feelslike, location)


# Get the forecast for the time specified.
def forecast(time, country, city):
    parsed_json = query('forecast', country, city)

    condition = parsed_json['forecast']['txt_forecast']['forecastday'][time]['fcttext_metric' if metric else 'fcttext']
    time = parsed_json['forecast']['txt_forecast']['forecastday'][time]['title']
    location = parsed_json['location']['city'] + ', ' + parsed_json['location']['state']
    return "Forecast for %s in %s: %s." % (time, location, condition)


# Get the forecast for the day.
def weather_forecast_today(country, city):
    return forecast(0, country, city)


# Get the forecast for next period of the day.
def weather_forecast_next(country, city):
    return forecast(1, country, city)


def get_conditions(l):
    return weather_current('Canada', l[0])


def get_forecast_today(l):
    return weather_forecast_today('Canada', l[0])


def get_forecast(l):
    return weather_forecast_next('Canada', l[0])


if __name__ == '__main__':
    #print weather_current('Canada', 'Toronto')
    #print weather_forecast_today('Canada', 'Toronto')
    #print weather_forecast_next('Canada', 'Toronto')

    print get_conditions(['Toronto'])
    print get_forecast_today(['Toronto'])
    print get_forecast(['Toronto'])

