from bitarray import bitarray
import bitarray.util as butil
import random
import math
import numpy as np

def bit_add(a, b):
    x = bitarray('0') + a
    y = bitarray('0') + b

    while y.any():
        carry = x & y
        x = x ^ y
        y = carry << 1
    x.pop(0)
    return x

def odd(num):
    odd = round(num)
    if odd % 2 == 0:
        odd += 1
    return odd

b = 3
r = 12
w = 16

message = input("Write message:\n")
print(message)
print(message.encode("utf-8"))
print(butil.hex2ba(message.encode("utf-8")))