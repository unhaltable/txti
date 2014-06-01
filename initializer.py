from parser import *
from api.cdf import lab
from api.dictionary import define, get_definition
from api.four_chan import four_chan
from api.jeffwu import jeff_wu_as_a_service
from api.rng import rng
from api.weather import get_conditions, get_forecast_today, get_forecast


def get_parser():
    parser = Parser()
    parser.addFormula(Formula("4chan", "4chan {{board}}", four_chan))
    parser.addFormula(Formula("cdf", "CDF {{lab}}", lab))
    parser.addFormula(Formula("dictionary", "Define {{word}}", define))
    parser.addFormula(Formula("jeff_wu_as_a_service", "Jeff Wu", jeff_wu_as_a_service))
    parser.addFormula(Formula("rng", "rng{{minmax}}", rng))
    parser.addFormula(Formula("weather_current", "Current weather in {{city}}", get_conditions))
    parser.addFormula(Formula("weather_forecast", "Forecast for {{city}}", get_forecast))
    parser.addFormula(Formula("weather_today", "Today's forecast for {{city}}", get_forecast_today))

    return parser

if __name__ == "__main__":
    print get_parser().parse("wat")