# h4XOR (75 points)

WU author: `inexp-mf`

## Statement
>Can you recover the _flag.png_ image?

Format: `Hero{flag}`

Author: `xanhacks`

## Solution


As [xor.py](xor.py) reads, the [_flag.png.enc_](flag.png.enc) is a result of XOR-ing the original _flag.png_ with a rather random (in terms of reproducing) key. The seed depended on the system time.

XOR-encoding is symmetrical: ```A xor B xor B = A```. 
That is, if we find out the original key and xor it with the _flag.png.enc_, hopefully we'll get the original _flag.png_.

Luckily for us, the key's length is fixed and known to be 9 = 8 + 1: 
```key = urandom(8) + bytes([randint(0, 9)])```

Moreover, the first 16 bytes of a png-file [are practically fixed](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html):
```89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52```
which stand for the png signature (8 B), IHDR chunk size (4 B, represents "13" as int32), chunk type (4 B, reads "IHDR"). One can get them from [any valid png](valid.png).

That's plenty. The key should satisfy the formula, then:
```key = flag.png.enc[:9] xor [89 50 4E 47 0D 0A 1A 0A 00]```

Let's try it out, find the key and decode our image. See [_decode.py_](decode.py) for details.

```key = b'^7\xd5l\xc7;`\xb3\t'```

Success!
The flag on the [_flag.png_](flag.png) reads: ```Hero{123_xor_321}```
