# Lost In Transmission

WU author: `inexp-mf`

## Statement
> I had my friend send me the flag, but it seems a bit...off.
Flag:
[flag.dat](flag.dat)

Author: `KNOX`

## Solution
Looks like nonsense in any encoding.
Caesar decoders don't give any fruits either. 
Let's look at bytecodes.
```py
with open('flag.dat','rb') as f:
    s = f.read()
b = [c for c in s]
print(b)

[230, 200, 198, 232, 204, 246, 174, 96, 220, 136, 102, 228, 204, 170, 152, 190, 218, 178, 190, 142, 96, 96, 200, 190, 230, 98, 164, 250]
```
Notice anything quirky about them?
They are all even. Then we are bound to have an idea:
```py
print(''.join([chr(c // 2) for c in b]))

sdctf{W0nD3rfUL_mY_G00d_s1R}
```
Yay, a flag!