from parser import *
from api.btc import get_btc_last, get_btc_high, get_btc_low, get_btc_volume, get_btc_vwap
from api.cdf import lab
from api.dictionary import define, get_definition
from api.four_chan import four_chan
from api.jeffwu import jeff_wu_as_a_service
from api.rng import rng
from api.weather import get_conditions, get_forecast_today, get_forecast


def get_parser():
    parser = Parser()
    parser.addFormula(Formula("4chan", "4chan {{board}}", four_chan))
    parser.addFormula(Formula("btc_last", "BTC last", get_btc_last))
    parser.addFormula(Formula("btc_high", "BTC high", get_btc_high))
    parser.addFormula(Formula("btc_low", "BTC low", get_btc_low))
    parser.addFormula(Formula("btc_vol", "BTC volume", get_btc_volume))
    parser.addFormula(Formula("btc_vwap", "BTC vwap", get_btc_vwap))
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