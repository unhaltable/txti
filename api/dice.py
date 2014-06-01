import random

def dice(l):
    i = int(l[0])
    nums = []
    while i > 0:
        nums.append(random.randint(1, int(l[1])))
        i-=1

    return reduce(lambda a,b: str(a) + ' ' + str(b), nums)

if __name__ == '__main__':
    print dice(['3', '20'])
