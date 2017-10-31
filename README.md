## Description
A simple Python class that mimics the size limitations of Intel x86/x64 registers. Useful when writing decoders and porting assembly to Python. Emulates common instructions that are used for manipulating bytes. This code is for anyone else tired of seeing 0xFF in their code. 

## Function Description 
object.FUNCTION(op1, op2, size) 

 * All functions are uppercase as to avoid confusion with standard Python functions. 
 * Same operand format as x86/x64 Intel Assembly. 
 * Size is specified by `l` for low byte, `h` for high byte, `w` for work, `d` for dword & `q` for qword. The default size is `dd` which specifies operand 1 is a dword and operand 2 is a dword. See `_get_size` for register examples and their size 
 * If the input is a string it will be converted to an int. 

# Status 
Beta. 

# Install 
```
git clone https://github.com/alexander-hanel/asmdec.git
cd asmdec
pip install .

```

## Example Usage:

```Python    
import struct 
from asmdec import *

def hasher(_str):
    a = AsmDec()
    init = bytearray(struct.pack("<L", 0x87654321))
    for count in range(0, 3):
        for cc, byte in enumerate(_str):
            # the "dd" size is default so the first one was left out as an example
            eax = init[a.AND(a.ADD(cc, count), 3, "dd")]
            temp = a.DEC(a.XOR(eax, byte, "ld"), "l")
            init[(cc + count & 3)] = temp
    return init

print hex(struct.unpack("<L", hasher("McTray.exe"))[0]) 
``` 
Output
```
0x923ca517
```

## Note
The `h` or high byte only reads and returns the byte value. For example if eax was `0xAABBCCDD`. Reading `ah` would return `0xCC`. 

```Python
>>> a = AsmDec()
>>> hex(a.FORMAT(0xAABBCCDD, 'h'))
'0xcc'
```
If `ah` was modified by adding `0x22` then `eax` would be `0xAABBEEDD`. If the code needs to mimic the 
high byte write use the `object.HIGHBYTE(value)` function to convert the byte to a high byte. 
```Python 
>>> hex(a.HIGHBYTE(0x22))
'0x2200'
>>> hex(a.ADD(0xAABBCCDD, a.HIGHBYTE(0x22)))
'0xaabbeedd'
```
