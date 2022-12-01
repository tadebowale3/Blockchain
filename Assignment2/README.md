# Assignment 02 - Bitcoin Script

Name    : Tanitoluwa Adebowale  
Email   : tadebowale@utexas.edu  
Discord : tadebowale3

## Program Inputs

The input of the script should be two hex-encoded strings of hash preimages, which have been verified to digest into an identical SHA1 hash (thereby demonstrating a hash collision).

```python
<196>
<14>
<7>
```

## Program Script

The script goes through the following operations:

```python
OP_DUP
OP_ADD
OP_MUL
OP_EQUAL
```

## Result

The `OP_EQUAL` result evaluates to true.

## Resources

**Script Wiz IDE**  
https://ide.scriptwiz.app
