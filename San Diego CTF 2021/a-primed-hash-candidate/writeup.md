# A Primed Hash Candidate
CRYPTO - MEDIUM

WU author: `inexp-mf`

## Statement
>After the rather embarrassing first attempt at securing our login, our student intern has drastically improved our security by adding more parameters. Good luck getting in now!
Server:
[server.py](server.py)
Connect via
`nc phc2.sdc.tf 1337`

Author: `RJ`

## Solution

What we have to do here is crack a xored and salted polynomial hash with all parameters kept in secret. If the password is incorrect, the server responds with its hash. Kind of a black box.
Let's pile up what we know from the code:
- A password is xored with `secret1` cycled.
- It is then extended with `secret2`.
- At last, it is used as coefficients for a polynomial with the base `secret3`, powers increasing from right to left.
- `secret3` is a 3-digit number.

Introducing some slang to use later:
- "To weighten" the string is to calculate from it a polynomial with the base `secret3`.
- "To flatten" is the reverse process. See the end of this write-up for a note on reversability of weightening in this task.
- "To tailcut" is to get a hash of a string, were salting with `secret2` not present at all. We, like, cut this tail off.

Shall we dive in?
1 . Determine hash difference for passwords that differ only in their least significant bit. Note: if strings differ in particular bits, they'll differ in the same bits after both xoring with whatever key. We'll use passwords "B" and "C", which have bitcodes "0100010" and "0100011".
```py
sB_h = 8775873360101286203205616007289582812832631170900
sC_h = 8553481739040134148226169955736135664968143909299
hashdiff = sC_h - sB_h
# -222391621061152054979446051553447147864487261601 (wow, 8th bit of secret1 must be 1)
```
2 . This difference equals _(+-1)secret3<sup>len(secret2)</sup>_. We then try to calculate _log<sub>s3</sub>(hashdiff)_ for s3 from 100 to 999 and see which one yields an integer suitable as a string's length. These s3 and integer are candidates for `secret3` and `len(secret2)`, respectively.
```py
from math import log

for b in range(100, 1000):
    log_ = log(hashdiff, b)
    if abs(log_ - int(log_)) < 1e-9:
        secret3 = b
        len_secret2 = int(log_)
        print(log_) # 20.0
        print(b)    # 233
```
Only one possible base satisfied the condition. Now we know: `secret3 == 233` and `len(secret2) == 20`.

3 . Now we're gonna find secret1. For that, we take a very long password, hopefully longer than secret1, say 'a'*50 and find it's xored version. Then we'll xor it with plain itself to get the `secret1`. Firstly, let's get its hash, call it h_a50.
```py
a50 = 'a'*50
h_a50 = 90322627272965138968526322287833333181628136566553607370678773792781245654017031843530006822120001131805244438354785222674398302080005346315921073929510528003964649
```
4 . Calculate the tailcut hash: subtract weighted secret2, which is exactly hash(""), and divide the result by secret3<sup>len(secret2)</sup>. 
A helpful formula that may look kinda ugly: 
![](equation.png)
```py
h_empty = 102600138716356059007219996705144046117627968461

def tailcut(h):
    h_tailcut = h - h_empty
    for _ in range(len_secret2):
        h_tailcut //= secret3

h_a50_tailcut = tailcut(h_a50)
```
We intentionally divide step-by-step, not using `**` or `pow`, in order for numbers to stay integral and not interfere with floating-point precision loss. "Insignificant" bits in large floats may steal a significant integer piece. Not appropriate for interger division.

5 . Flatten the tailcut hash. We got `xored_a50 = ('a'*50) xor cycle(secret1)`. So `cycle(secret1) = xored_a50 xor a50`, because xor transform is symmetrical. It's easy then to determine `secret1` from its repeated version.
```py
def flatten(h):
    res = []
    while h >= b:
        res.append(h % secret3)
        h //= secret3
    res.append(h)
    return [chr(int(c)) for c in res][::-1]

xored_a50 = flatten(h_a50_tailcut)

def xor(data, key):
    ''.join(chr(ord(c) ^ ord(k)) for c,k in zip(data, cycle(key)))

print(xor(xored_a50, a50))
# el3PH4nT$el3PH4nT$el3PH4nT$el3PH4nT$el3PH4nT$el3PH
secret1 = "el3PH4nT$"
```
6. Let's reverse the target hash. Do step 4 for it, then flatten and finally xor with `secret1`.
```py
PASSWD = 91918419847262345220747548257014204909656105967816548490107654667943676632784144361466466654437911844
password = xor(flatten(tailcut(PASSWD)), secret1)
print(password) # GZZ9t3W3Ar34un44m8PLXX6
```
It's a good sign that all characters of the password are within alnum ASCII subset. Let's try it out then. 
Success, and the flag is `sdctf{W0W_s3cur1ty_d1d_dRaStIcAlLy_1mpr0v3}`. It sure did.

It's worth mentioning that have not just found a collision, we have effectively reversed the hash. And it's thanks to `secret3` being larger than 127. Otherwise, at every step of flattening we would probably be in the same indecisiveness that made `"a-prime-hash-candidate"` an actual challenge.