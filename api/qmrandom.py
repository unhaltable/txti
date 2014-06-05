import random
import requests



url = "https://qrng.anu.edu.au/API/jsonI.php?length={}&type={}&size={}"



class qmrandom(random.Random):

    def __init__(self):
        self.nums = []
        super(qmrandom, self).__init__()

    def seed(self, x=None):
        pass

    def random(self):
        if (len(self.nums) == 0):
            self._getNums()
        return int(self.nums.pop(), 16) / (16 ** 8)

    def getstate(self):
        pass

    def setstate(self):
        pass

    def _getNums(self):
        r = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length=100&type=hex16&size=4", verify=False)
        j = r.json()
        self.nums = j["data"]

_inst = qmrandom()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits

if __name__ == "__main__":
    x = qmrandom()
    for i in range(1000):
        print(x.random())

