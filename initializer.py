from parser import *
from api.bitly import shorten_url
from api.btc import get_btc_info
from api.calc import calc
from api.cdf import lab
from api.dictionary import define, get_definition
from api.four_chan import four_chan
from api.jeffwu import jeff_wu_as_a_service
from api.nextbus import get_bus_prediction
from api.rng import rng
from api.tips_calc import calc_tip
from api.rotten import get_movie
from api.doge import get_doge_info
from api.weather import get_conditions, get_forecast_today, get_forecast
from api.dice import dice
from api.fakeapi import fake_an_api

def get_parser():
    parser = Parser()
    parser.addFormula(Formula("4chan", "4chan {{board}}", four_chan, ee=True))
    parser.addFormula(Formula("bitly", "Shorten {{url}}", shorten_url))
    parser.addFormula(Formula("btc", "BTC", get_btc_info))
    parser.addFormula(Formula("calc", "Calc {{formula}}", calc))
    parser.addFormula(Formula("cdf", "CDF {{lab}}", lab))
    parser.addFormula(Formula("dictionary", "Define {{word}}", define))
    parser.addFormula(Formula("jeff_wu_as_a_service", "Jeff Wu", jeff_wu_as_a_service, ee=True))
    parser.addFormula(Formula("next_bus", "Next bus for {{routedirectionintersection}}", get_bus_prediction))
    parser.addFormula(Formula("rng", "rng{{minmax}}", rng))
    parser.addFormula(Formula("tips", "Tip {{amountpercent}}", calc_tip))
    parser.addFormula(Formula("rotten_tomatoes", "Rotten {{movie}}", get_movie))
    parser.addFormula(Formula("weather_current", "Current weather in {{city}}", get_conditions))
    parser.addFormula(Formula("weather_forecast", "Forecast for {{city}}", get_forecast))
    parser.addFormula(Formula("weather_today", "Today's forecast for {{city}}", get_forecast_today))
    parser.addFormula(Formula("reverse", "Reverse {{string}}", lambda l: l[0][::-1]))
    parser.addNoParamFormula("always_cancer", "I feel sick", "it's probably cancer (but consult a real doctor)")
    parser.addFormula(Formula("doge", "doge", get_doge_info))
    parser.addFormula(Formula("dice", "Roll {{n}} D {{x}}", dice))
    parser.addFormula(Formula("fakeapi_user", "fakeapi", fake_an_api, auth=True))

    return parser

if __name__ == "__main__":
    print get_parser().parse("Roll 4 D 20")
    print get_parser().parse("I feel sick")
    print get_parser().parse("list")
    print get_parser().parse("Donate 5 USD")
