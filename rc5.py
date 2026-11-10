import random
import sys
import math
import numpy as np
from bitarray import bitarray
import bitarray.util as butil

def bit_add(a, b):
    x = bitarray('0') + a
    y = bitarray('0') + b

    while y.any():
        carry = x & y
        x = x ^ y
        y = carry << 1
    x.pop(0)
    return x

def encrypt(w, r, b):
    key = random.randint(1,pow(2,(8*b))-1)
    key = bin(key)[2:]
    if len(key) < (8*b):
        remainder = (8*b) - len(key)
        key = bitarray('0'*remainder) + key
    s_table = s_table(w, r, b, key)
    
    

def decrypt(w, r, b, cipher, key):
    if cipher == "":
        cipher = input("Input Ciphertext Here:\n")
    if key == "":
        key = input("Input Key Here\n")
    

def s_table(w, r, b, key):
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



def odd(num):
    odd = round(num)
    if odd % 2 == 0:
        odd += 1
    return odd

def demo(w, r, b):
    cipher, key = encrypt(w, r, b)
    decrypt(w, r, b, cipher, key)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("user must define world length in bits(w), rounds(r), and key size in bytes(b)")
    w = sys.argv[1]
    r = sys.argv[2]
    b = sys.argv[3]
    while True:
        menu = input("Select Mode:\n" \
        "1) Encrypt Message\n" \
        "2) Decrypt Message\n" \
        "3) Demo Both\n" \
        "4) Quit\n")

        match menu:
            case "1":
                encrypt(w, r, b)
            case "2":
                decrypt(w, r, b, "", "")
            case "3":
                demo(w, r, b)
            case "4":
                sys.exit(0)
            case _:
                print("Please select 1, 2, 3, or 4")
