from parser import *
from api.rng import rng
from api.jeffwu import jeff_wu_as_a_service
from api.cdf import get_lab

def getParser():
    parser = Parser()
    parser.addFormula(Formula("rng", "rng{{minmax}}", rng))
    parser.addFormula(Formula("jeff_wu_as_a_service", "Jeff Wu", jeff_wu_as_a_service))
    parser.addFormula(Formula("cdf", "CDF {{lab}}", get_lab))

    return parser

