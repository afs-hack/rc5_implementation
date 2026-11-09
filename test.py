from bitarray import bitarray
import random
import math
import numpy as np



def odd(num):
    odd = round(num)
    if odd % 2 == 0:
        odd += 1
    return odd

b = 5
r = 12
w = 64

key_start = random.randint(1,pow(2,(8*b))-1)
key = bin(key_start)[2:]
print(len(key))
if len(key) < (8*b):
    remainder = (8*b) - len(key)
    key_end = key
    key = bitarray('0'*remainder)
    key.extend(key_end)
    
t = 2 * (r+1)
u = w/8
c = math.ceil(b/u)
e = math.e
phi = (1 + math.sqrt(5)) / 2
p = odd((e - 2)*(pow(2,w)))
q = odd((phi - 1)*(pow(2,w)))

#Convert the Key from Bytes to words
l = []
for i in range(c):
    if w*(i+1) > len(key):
        remainder = w*(i+1) - len(key)
        last_word = bitarray('0'*remainder)
        last_word.extend(key[-len(key):w*i])
        l.append(last_word)
    l.append(key[-w*(1+i):-w*i])
#Initialize S
s = []
s.append(bitarray(bin(p)[2:]))
for i in range(1, t):
    s.append(s[i-1] + bitarray(bin(q)[2:]))
#Mix in Key
i = j = 0
A = B = bitarray('0'*w)
for times in range(3 * max(t,c)):
    A = s[i] = (s[i] + A + B).rotate(3)
    B = l[j] = (l[j] + A + B).rotate(A+B)
    i = (i + 1) % t
    j = (j + 1) % c