# A Bowl of Pythons
REVENGE - EASY

WU author: `inexp-mf`

## Statement
> A bowl of spaghetti is nice. What about a bowl of pythons?
[chal.py](chal.py)

Author: `k3v1n`

## Solution
The code is poorly obfuscated. I'm not gonna eval any string the content of which I don't know. So let's unobfuscate it first.
```py
#! /usr/bin/env python3
FLAG = 'sdctf{a_v3ry_s3cur3_w4y_t0_st0r3_ur_FLAG}' # lol

a = lambda n: a(n-2) + a(n-1) if n >= 2 else (2 if n == 0 else 1)

b = lambda x: bytes.fromhex(x).decode()

h = print

def d():
    print('Incorrect flag! You need to hack deeper...')
    __import__("sys").exit(1)
    h(FLAG)

def e(f):
    print("Welcome to SDCTF's the first Reverse Engineering challenge.")
    c = input("Input the correct flag: ")
    if c[:6] != 'sdctf{':
        d()
    if c[-1] != '}':
        d()
    g = c[6:-1].encode()
    if bytes( (g[i] ^ (a(i) & 0xff) for i in range(len(g))) ) != f:
        d()
    print('Nice job. You got the correct flag!')

if __name__ == "__main__":
    e(b't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4')
else:
    __import__("sys").exit(0)
``` 
The remaining question is, what happens here?
```py
if bytes( (g[i] ^ (a(i) & 0xff) for i in range(len(g))) ) != f:
```
`a(i)` generates the i-th Fibonacci number. `a(i) & 0xff` takes the modulo 256.
So the variable part of the flag is encoded, xored with Fibonacci numbers mod 256, and this is how f was made. \
Once again for this CTF, xor is a symmetrical transform. If we xor f with the same Fibonacci numbers mod 256, we get the flag:
```py
a = lambda n: a(n-2) + a(n-1) if n >= 2 else (2 if n == 0 else 1)
f = b't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4'
bytes((f[i] ^ (f(i) & 0xff) for i in range(len(f))))
```
`b'v3ry-t4sty-sph4g3tt1'`

Yummy! The flag is `sdctf{v3ry-t4sty-sph4g3tt1}`.
