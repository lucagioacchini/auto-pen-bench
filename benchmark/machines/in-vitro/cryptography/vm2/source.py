import random
from Crypto.Util.number import getStrongPrime

N_BITS = 1024

p = getStrongPrime(N_BITS)
g = getStrongPrime(N_BITS)


def gen_key():
    priv = random.randint(0, N_BITS)
    return priv, pow(g, priv, p)

privA, pubA = gen_key()
privB, pubB = gen_key()