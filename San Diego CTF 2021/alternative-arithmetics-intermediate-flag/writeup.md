# Alternative Arithmetic (Intermediate Flag)
MISC - MEDIUM

WU author: `inexp-mf`

## Statement
> Java has provided an alternative mathematical system. Please submit only the intermediate flag for this challenge.
Connect via
`nc java.sdc.tf 1337`

Author: `k3v1n`

## Solution
Let's connect and face the the riddles.
```
$ nc java.sdc.tf 1337

Welcome to the 1337 Java quiz!
Make sure you learn its quirks before you start this journey.
Answer all questions to the best of your ability. Do not input any semicolons.
Good luck!


1. Find a nonzero `long x` such that `x == -x`, enter numbers only, no semicolons:
x =
```
After a couple of open sources about the primitive `long` type and signed integers representation, following clues are apparent:
- Negative integers are represented as two's complement. 
That is, non-negative numbers are bitwise stored as-is: from 0 = `00...0`(64 zeros) up to 2<sup>63-1</sup>= `011...1`(zero and 63 ones); 
while negative numbers start with -2<sup>63</sup>=`100...0`(1 one and 63 zeros), end with -1=`11...1`(64 ones);
and numbers are effeciently negated the following way: all bits are inverted and `000...01` is added.
FYI this transform is symmetrical.
Such representation allows summing signed longs with the same ALUs as for unsigned longs and also negating numbers fast.
- Integers are compared bitwise.

That explains why essentially `0 == -0`:
`00...0` inverted is `11...1`, add `1` and we get an overflow `1|00...0`(1 overflowing one and 64 zeros) which is practically zero again.

And it also hints how to find another number which is its own two's complement.
Aaand it's `long.MIN_VALUE`, i.e. -2<sup>63</sup>, i.e. `100...0`, i.e. `-9223372036854775808`
Invert it and you get `011...1`. Add `1` and you get `100...0` again. Magic!
```
x = -9223372036854775808
Perfect! You are correct.

2. Find 2 different `long` variables `x` and `y`, differing by at most 10, such that `Long.hashCode(x) == Long.hashCode(y)`:
x =
```
Let's search for sources without further ado.
...
Okay, I'm back. Been [here](http://hg.openjdk.java.net/jdk8/jdk8/jdk/file/f92ab6dbbff8/src/share/classes/java/lang/Long.java), found this:
```
public static int hashCode(long value) {
    return (int)(value ^ (value >>> 32));
}
```
Essentially, this happens: split a number into major and minor halves, each of 32 bits, and xor them bitwise.
I suggest, we search around 0. Bit representations drastically change there, while values don't.
Note that for any number, it's bitwise negation will have the same hashcode. 
Well, we already know that `x` negated bitwise is `-x - 1`.
So, 0 and -1, 1 and -2,... 4 and -5 should all meet the condition. Let's try 4 and -5.
```
x = 4
y = -5
Perfect! You are correct.

3. Enter a float value f that makes the following function return true: 
```
```java
boolean isLucky(float magic) {
    int iter = 0;
    for (float start = magic; start < (magic + 256); start++) {
        if ((iter++) > 2048) {
            return true;
        }
    }
    return false;
}
```
This one is also a puzzle on weird liminal behavior, this time of floats. And this one is also more practically important.
[IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) describes the binary float format: `s|eeeeeeee|ccccccccccccccccccccccc` - 1-bit sign, 8-bit binary exponent, 23-bit normalized fraction.
Say, two floats are added. If exponents differ then the absolutely lesser one's fraction is shifted right to the amount of exponents' difference and then fractions can be added like unsigned integers. Not the larger one is shifted, in order to lose least significant bits, not the most ones, in case of precision loss.
Well, when exponents differ by more than 23, the lesser addend's fraction is shifted down to 0.
In our case we want the for the cycle to complete 2048 > 256 iterations. Knowing the precision loss mechanics, we may choose a `magic` value big enough for 1 at increment to be shifted to 0 when it's added. So the cycle's end condition is never met.
More precisely, we want `magic` to be at least 2<sup>24</sup>. Let's try 2<sup>23</sup> and then 2<sup>24</sup>:
```
f = 8388608 
Sorry, your answer is not correct. Try something else next time.
...
f = 16777216
Your input must be less than 7 characters long (excluding newlines).
```
That's just sad. Yet there's another rather short notation, `1e8`, which gives us a number slighly larger than the one we want.
```
f = 1e7
Sorry, your answer is not correct. Try something else next time.
...
f = 1e8 
Perfect! You are correct.

Good job. You earned the intermediate flag:
sdctf{JAVA_Ar1thm3tIc_15_WEirD}
To get the final flag please answer 2 more questions.
```
We are not doing this in this task. The intermediate flag is ours.