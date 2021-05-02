# Atoms (50 points)

WU author: `inexp-mf`

## Statement
>Dmitri sends us this message, will you be able to retrieve the secret message hidden inside?
`MtMdDsFmMdHsMdMdUuo`

Format: `Hero{flag}`

Author: `xanhacks`

## Solution
"Dmitri", "Atoms" and camel-cased abbreviations from the message all point out to the periodic table.

Bet this is a variation on the Vigenère cipher. Let us replace the elements in the message with their respective table numbers and see where it takes us.
![Credit: IUPAC. Thanks, IUPAC!](https://iupac.org/wp-content/uploads/2018/12/IUPAC_Periodic_Table-01Dec18.jpg)

>`[109, 101, 110, 100, 101, 108, 101, 101, 118]`

Looks like ASCII codes. Of latin letters. In lowercase.

More recent versions of the table call the 118-th element "Oganesson - Og" instead of its initial name "Ununoctium - Uuo" which stood for the number 118. But you totally would guess the last letter, were it not even given at all.

Let us decode the cipher with a simple py-script:
```python
encoded = [109, 101, 110, 100, 101, 108, 101, 101, 118]
print(''.join(chr(c) for c in encoded)) # mendeleev
```

So the flag is: 
>`Hero{mendeleev}`