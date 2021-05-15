# A Prime Hash Candidate
CRYPTO - EASY

WU author: `inexp-mf`

## Statement
>We hired a fresh MATH 187A student to create our login for us. After 6 months of backbreaking development, we're no longer storing passwords as plain text. Just try to break in!
Hash function:
[server.py](server.py)
Connect via
`nc phc1.sdc.tf 1337`

Author: `RJ`

## Solution
A brief statement summary:
We are given a polynomial hash function and the hash of the target password. We should find a password having hash such as the given one (aka a collision) and authorize with it. They literally said they don't store passwords as plain text.

To reverse the hash, we can simply repeatedly subtract the remainder, save it as another character from the password and divide the hash further:
```python
passwd.append(hash % 31)
hash -= passwd[-1]
hash //= 31
```
Or can we?
The problem is, all printable ASCII characters have codes larger than 31. Which means, when we try to reverse the hashing process, at each step we are generally indecisive about which charcode stands for the remainder `mod = hash // 31`: mod + 31, mod + 62, mod + 93 or mod + 124?
For instance, calculate a hash of `"00" == chr(48) * 2`. It is `48 + 48 * 31 = 1519`. The following strings will have the same hash: `"O/", "n."`

That's why we might wanna try to bruteforce it in some clever way, i.e. narrowing the character set and stopping after some time.

We'll recursively try and bite off a suitable charcode at every step until the leftover of the hash is 0 or less.

The code below yields us a lot of collisions for the printable ASCII charset, with some promising results amid them:
```py
hsh = 59784015375233083673486266

suffixes = []
alphabet = set(range(32, 128))
def step(h, suffix):
    if h == 0:
        print(''.join(suffix[::-1]))
    if h < 0:
        return
    if len(suffixes) == 1000000:
        print("many")
    if len(suffixes) > 1000000:
        return
    mod = h % 31
    for asci in [mod + 31, mod + 62, mod + 93, mod + 124]:
        if asci not in alphabet:
            continue
        step((h - asci) // 31, suffix + chr(asci))
```
```
...
Oa4SWORD_I#5*+0')
Q"SSWORD_I#5*+0')
PASSWORD_I#5*+0')
O`SSWORD_I#5*+0')
NSSWORD_I#5*+0')
...
```

After playing around a little, I found out that even the latin alnum charset with "_" (but not without it, smh) yields a pile of collisions:
```py
alphabet = {ord(c) for c in
           'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'}
```
```
...
PB4SWORD_HASHINEH
Oa4SWORD_HASHINEH
PASSWORD_HASHINEH - is that our boy or just something quite alike?
O_rSWORD_HASHINEH
PB3rWORD_HASHINEH
...
```

After all, any of these collisions is suitable as the password:
```
$ nc phc1.sdc.tf 1337
Please enter password below
PB4T7nRD_HB4HINEH
Login successful!
Flag: sdctf{st1ll_3553nt14lly_pl@1n_txt}
```
