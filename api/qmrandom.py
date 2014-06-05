import random
import requests



url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=hex16&size=4"

def _getSeed():
    r = requests.get(url, verify=False)
    j = r.json()
    num = j["data"][0]
    i = int(num, 16)
    print(i)
    return i

class qmrandom(random.Random):

    def seed(self):
        super.seed(_getSeed())

    def random(self):
        self.seed()
        return super.random()

if __name__ == "__main__":
    _getSeed()