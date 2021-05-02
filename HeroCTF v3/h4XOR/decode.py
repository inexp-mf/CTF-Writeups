#!/usr/bin/env python3
#from pwn import xor
from itertools import cycle

def xor(data, key): # if you haven't installed pwntools and are too lazy to
    return b''.join((c ^ k).to_bytes(1, 'big') for c,k in zip(data, cycle(key)))

with open("valid.png", 'rb') as input:
    first_9_bytes = input.read(9)

with open("flag.png.enc", "rb") as input:
    encoded = input.read()
    key = xor(encoded[:9], first_9_bytes)   # b'^7\xd5l\xc7;`\xb3\t'
    
    with open("flag.png", "wb") as output:
        output.write(xor(encoded, key))
