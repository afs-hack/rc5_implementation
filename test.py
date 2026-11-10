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

key = random.randint(1,pow(2,(8*b))-1)
key = bin(key)[2:]
if len(key) < (8*b):
    remainder = (8*b) - len(key)
    key = bitarray('0'*remainder) + key
    
t = 2 * (r+1)
u = w/8
c = math.ceil(b/u)
e = math.e
phi = (1 + math.sqrt(5)) / 2
p = odd((e - 2)*(pow(2,w)))
q = odd((phi - 1)*(pow(2,w)))

print(len(bin(p)[2:]))
print(key[-16:0])

#Convert the Key from Bytes to words
l = []
for i in range(c):
    if w*(i+1) > len(key):
        remainder = w*(i+1) - len(key)
        last_word = bitarray('0'*remainder)
        last_word.extend(key[-len(key):-w*i])
        l.append(last_word)
    else:
        l.append(bitarray(key[-w*(1+i):-w*i or None]))
#Initialize S
s = []
s.append(bitarray(bin(p)[2:]))
for i in range(1, t):
    s.append(bit_add(s[i-1],bitarray(bin(q)[2:])))
#Mix in Key
i = j = 0
A = B = bitarray('0'*w)
for times in range(3 * max(t,c)):
    A = s[i] = (bit_add(s[i], bit_add(A,B)))
    A.rotate(3), s[i].rotate(3)
    B = l[j] = (bit_add(l[j], bit_add(A,B)))
    B.rotate(butil.ba2int(bit_add(A,B)) % w), l[j].rotate(butil.ba2int(bit_add(A,B)) % w)
    i = (i + 1) % t
    j = (j + 1) % c