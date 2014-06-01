import __future__
from decimal import Decimal

def calc_tip(l):
    formula = '{} * ({} / 100)'.format(l[0], l[1])
    amount = str(eval(compile(formula, '<string>', 'eval', __future__.division.compiler_flag)))
    dec_amt = Decimal(amount)
    return '$' + str(dec_amt.quantize(Decimal('1.00')))


if __name__ == '__main__':
    print calc_tip(['20.00', '5'])  # 1
    print calc_tip(['15.75', '12'])  # 1.89