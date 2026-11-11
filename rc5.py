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

def bit_sub(a, b):
    one = bitarray('0' * (len(b) - 1) + '1')
    return bit_add(a, bit_add(~b, one))

def odd(num):
    odd = round(num)
    if odd % 2 == 0:
        odd += 1
    return odd

def s_table(w, r, b, key):
    t = 2 * (r+1)
    u = w/8
    c = max(1, math.ceil(b/u))
    e = math.e
    phi = (1 + math.sqrt(5)) / 2
    p = odd((e - 2)*(pow(2,w)))
    q = odd((phi - 1)*(pow(2,w)))

    #Convert the Key from Bytes to words
    padded_key = butil.zeros(c*w - len(key)) + key
    l = []
    for i in range(c):
        l.append(padded_key[-w*(1+i):-w*i or None])
    #Initialize S
    s = []
    s.append(bitarray(bin(p)[2:]))
    for i in range(1, t):
        s.append(bit_add(s[i-1],bitarray(bin(q)[2:])))
    #Mix in Key
    i = j = 0
    A = B = bitarray('0'*w)
    for times in range(3 * max(t,c)):
        A = (bit_add(s[i], bit_add(A,B)))
        A.rotate(-3)
        s[i] = A
        rot_amt = (butil.ba2int(bit_add(A, B)) % w) * -1
        B = (bit_add(l[j], bit_add(A, B)))
        B.rotate(rot_amt)
        l[j] = B
        i = (i + 1) % t
        j = (j + 1) % c
    return s

def encrypt(w, r, b):
    #Size of s_table
    t = 2 * (r+1)
    #Generate key of size b bytes
    key = random.randint(1,pow(2,(8*b))-1)
    key = bitarray(bin(key)[2:])
    if len(key) < (8*b):
        remainder = (8*b) - len(key)
        key = bitarray('0'*remainder) + key
    #Generate S_Table
    s = s_table(w, r, b, key)
    #Take Message as input and convert into bitarray
    message = bitarray()
    message.frombytes(input("Write message here:\n").encode("utf-8"))
    message.fill(2*w)
    #Turn message into an array of words
    m_arr = []
    for i in range(int(len(message)/w)):
        m_arr.append(message[i*w:(i+1)*w])
    #Encrypt all words in message
    c_arr = []
    for i in range(0, len(m_arr)-1, 2):
        A = bit_add(m_arr[i], s[0])
        B = bit_add(m_arr[i+1], s[1])
        for j in range(1,r+1):
            A = A ^ B
            A.rotate((butil.ba2int(B) % w) * -1)
            A = bit_add(A, s[2 * j])
            B = A ^ B
            B.rotate((butil.ba2int(A) % w) * -1)
            B = bit_add(B, s[2 * j + 1])
        c_arr.append(A)
        c_arr.append(B)
    cipher = bitarray()
    #Convert words back into string
    for c in c_arr:
        cipher += c
    cipher = butil.ba2hex(cipher)
    key = butil.ba2hex(key)
    print(f"Key is:\n{key}")
    print(f"Ciphertext is:\n{cipher}")
    return cipher, key

    

def decrypt(w, r, b, cipher, key):
    if cipher == "":
        cipher = input("Input Ciphertext Here:\n")
    if key == "":
        key = input("Input Key Here\n")
    t = 2 * (r + 1)
    #Convert cipher and key to bitarrays
    cipher = butil.hex2ba(cipher)
    key = butil.hex2ba(key)
    #Generate s_table
    s = s_table(w, r, b, key)
    #convert cipher into and array of words
    c_arr = []
    for i in range(int(len(cipher)/w)):
        c_arr.append(cipher[i*w:(i+1)*w])
    m_arr = []
    for i in range(0, len(c_arr) - 1, 2):
        B = c_arr[i+1]
        A = c_arr[i]
        for j in range(r, 0, -1):
            B = bit_sub(B, s[2 * j + 1])
            B.rotate(butil.ba2int(A) % w)
            B = B ^ A
            A = bit_sub(A, s[2 * j])
            A.rotate(butil.ba2int(B) % w)
            A = A ^ B
        B = bit_sub(B, s[1])
        A = bit_sub(A, s[0])
        m_arr.insert(0,B)
        m_arr.insert(0,A)
    message = bitarray()
    for m in m_arr:
        message += m
    message = message.tobytes().rstrip(b"\x00").decode("utf-8")
    print(f"Message is:\n{message}")
    return message


def demo(w, r, b):
    cipher, key = encrypt(w, r, b)
    decrypt(w, r, b, cipher, key)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("user must define world length in bits(w), rounds(r), and key size in bytes(b)")
    w = int(sys.argv[1])
    r = int(sys.argv[2])
    b = int(sys.argv[3])
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
