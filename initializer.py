from parser import *
from api.rng import rng
from api.jeffwu import jeff_wu_as_a_service
from api.cdf import get_lab
from api.four_chan import four_chan
from api.weather import weather_current
from api.weather import weather_forecast_today
from api.weather import weather_forecast_next

def getParser():
    parser = Parser()
    parser.addFormula(Formula("rng", "rng{{minmax}}", rng))
    parser.addFormula(Formula("jeff_wu_as_a_service", "Jeff Wu", jeff_wu_as_a_service))
    parser.addFormula(Formula("cdf", "CDF {{lab}}", get_lab))
    parser.addFormula(Formula("4chan", "4chan {{board}}", four_chan))
    parser.addFormula(Formula("weather_current", "Current weather in {{city}}", weather_current))
    parser.addFormula(Formula("weather_today", "Today's forecast for {{city}}", weather_forecast_today))
    parser.addFormula(Formula("weather_forecast", "Forecast for {{city}}", weather_forecast_next))

    return parser

if __name__ == "__main__":
    print getParser().parse("wat")