from parser import *
from api.cdf import get_lab
from api.dictionary import get_definition
from api.four_chan import four_chan
from api.jeffwu import jeff_wu_as_a_service
from api.rng import rng
from api.weather import weather_current
from api.weather import weather_forecast_next
from api.weather import weather_forecast_today


def get_parser():
    parser = Parser()
    parser.addFormula(Formula("4chan", "4chan {{board}}", four_chan))
    parser.addFormula(Formula("cdf", "CDF {{lab}}", get_lab))
    parser.addFormula(Formula("dictionary", "Define {{word}}", get_definition))
    parser.addFormula(Formula("jeff_wu_as_a_service", "Jeff Wu", jeff_wu_as_a_service))
    parser.addFormula(Formula("rng", "rng{{minmax}}", rng))
    parser.addFormula(Formula("weather_current", "Current weather in {{city}}", weather_current))
    parser.addFormula(Formula("weather_forecast", "Forecast for {{city}}", weather_forecast_next))
    parser.addFormula(Formula("weather_today", "Today's forecast for {{city}}", weather_forecast_today))

    return parser

if __name__ == "__main__":
    print get_parser().parse("wat")
