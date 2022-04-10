import random
from datetime import datetime

random.seed(datetime.now())
for ii in range(10000):
    nn = random.randint(1, 1000)
    if nn % 2 == 0:
        print("ADD ", nn)
    else:
        print("DEC ", nn)