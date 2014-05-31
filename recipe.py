__author__ = 'jonathanwebb'
from plex import *
import cStringIO

class Parser:

    def __init__ (self):
        self.formulae = {} ## dict of string to Formula objects
        self.lex = [] ## list of lexical rules

    def addFormula(self, formula):
        if (self.__checkIfIDUsed(formula.id)):
            raise DuplicateIDException
        else:
            self.formulae[formula.id] = formula


    def __checkIfIDUsed(self, id):
        for key in self.formulae.keys():
            if id == key:
                return True
        return False


class Formula:

    def __init__(self, id, formula, f):
        '''
        :param id: str
        :param formula: str
        :param f: str
        :return: None
        '''

        self.func = f
        self.id = id

        letter = Range("AZaz")
        digit = Range("09")
        text = Rep(letter | digit | Str(" "))
        open_bracket = Str('{{')
        close_bracket = Str('}}')
        lex = Lexicon([
            (text, 'terminal'),
            (open_bracket, 'open'),
            (close_bracket, 'close')
        ])
        s = cStringIO.StringIO(formula)
        scanner = Scanner(lex, s)

        tokens = []
        while 1:
            token = scanner.read()
            if token[1] is '':
                break
            else:
                tokens.append(token)

        lexl = []
        param = False
        for instance in tokens:
            if instance[0] == 'terminal':
                if (param):
                    lexl.append((instance[1], self.id + '_terminal'))
                else:
                    lexl.append((instance[1], self.id + '_id'))
            elif(instance[0] == 'open'):
                param = True
            elif(instance[0] == 'close'):
                param = False

        for x in lexl:
            print x

class DuplicateIDException(Exception):
    pass

def testfunc():
    print "x"

if __name__ == '__main__':
    Formula('testfunc', 'Next bus for {{route}} at {{intersection}}', testfunc)