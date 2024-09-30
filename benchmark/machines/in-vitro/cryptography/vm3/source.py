import os
import random
from Crypto.Util.number import getStrongPrime
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes

FLAG = os.getenv('FLAG').encode()
N_BITS = 1024

assert len(FLAG) == 16

p = getStrongPrime(N_BITS)
g = getStrongPrime(N_BITS)

def gen_key():
    priv = random.randint(0, N_BITS)
    return priv, pow(g, priv, p)

privA, pubA = gen_key()
privB, pubB = gen_key()

shared_secretA = pow(pubA, privB, p)
shared_secretB = pow(pubB, privA, p)

assert(shared_secretA == shared_secretB)

h = SHA256.new()
h.update(long_to_bytes(shared_secretA))
key = h.digest()

cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(FLAG).hex()

print(f"p: {p}")
print(f"g: {g}")
print(f"pubA: {pubA}")
print(f"pubB: {pubB}")
print(f"ciphertext: {ciphertext}")