# Case64AR
CRYPTO - EASY

WU author: `inexp-mf`

## Statement
> Someone script kiddie just invented a new encryption scheme. It is described as a blend of modern and ancient cryptographic techniques. Can you prove that the encryption scheme is insecure by decoding the ciphertext below?
Ciphertext
`OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv`

Author: `k3vin`

## Solution
The caption and other clues suggest that two encodings were combined somehow: base64 and Caesar cipher. The question is, how exactly?

The simplest options:
- Caesar within ASCII, then base64.
Let's try it out to no avail:
```py
import base64 as b64
enc  = 'OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv'
decoded = b64.b64decode(enc)
for shift in range(128):
    shifted = ''.join(chr((c + shift) % 128) for c in decoded)
    print(shifted)
```
None of the strings looks like a flag or anything meaningful.
- base64, then Caesar. 
Seems unlike because the ciphertext is still in base64 character range. Unless the translation table is not ASCII but the base64 alphabet instead?
Let's check this one:
```py
import base64 as b64
table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
untable = {table[i]:i for i in range(len(table))}
enc  = 'OoDVP4LtFm7lKnHk+JDrJo2jNZDROl/1HH77H5Xv'
for shift in range(len(table)):
    shifted = ''.join(table[(untable[c] + shift) % len(table)] for c in enc)
    try:
        print(b64.b64decode(shifted))
    except:
        print(f'Failed on {shift}')
```
Among others:
```b'sdctV{OB3cUr-ty_`\xf1nt_s3\x02UR\x08Ti}'```

We're obviously close. Let's try without `=` in the alphabet:
```b'sdctf{OBscUr1ty_a1nt_s3CURITy}```

Success!