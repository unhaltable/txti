from parser import *
from api.rng import rng

def getParser():
    parser = Parser()
    parser.addFormula(Formula("rng", "rng{{minmax}}", rng))



    return parser

