import __future__

def calc(l):
    return eval(compile(l[1:], '<string>', 'eval', __future__.division.compiler_flag))

if __name__ == '__main__':
    print calc(['2 + 2'])
    print calc(['2 / 2 + 1 - 50'])
    print calc(['5 / 2'])