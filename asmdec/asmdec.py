#!/usr/bin/env python

"""asm_dec.py: python class that aids with x86/x64 register sizes"""

__author__ = "Alexander Hanel"
__version__ = "1.0.0"

"""
Description:
    * Simple Python class that mimics the size limitations of Intel x86/x64 registers. Useful 
    for when writing decoders and porting assembly to python. Emulates common instructions 
    that are used for manipulating bytes. 
    * object.FUNCTION(op1, op2, size) 
        - all functions are uppercase as to avoid confusion with standard Python functions 
        - same operand format as Assembly. 
        - size is specified by l for low byte, h for high byte, w for work, d for dword & 
          q for qword. The default size is "dd" which specifies operand 1 is a dword and 
          operand 2 is a dword. See _get_size for register examples and their size 
    * Example Usage:
    
        import struct 
        def hasher(_str, size):
            a = AsmDec()
            init = bytearray(struct.pack("<L", 0x87654321))
            for count in range(0,3):
                for cc, byte in enumerate(_str):
                    # the "dd" size is default so could be left out 
                    eax = init[a.AND(a.ADD(cc, count, "dd"), 3, "dd")]
                    temp = a.DEC(emu.XOR(eax, byte, "ld"), "l")
                    init[(cc + count & 3)] = temp
            return str(init)    

    * Note: The h or high byte only reads and returns the byte value. For example if eax was 0xAABBCCDD. 
            Reaading ah would retunr 0xCC. 
            >>> a = AsmDec()
            >>> hex(a.FORMAT(0xAABBCCDD, 'h'))
            '0xcc'
            but if ah was modified by adding 0x22 then eax would be 0xAABBEEDD. If the code needs to mimic the 
            high byte write use the object.HIGHBYTE(value) function to convert the byte to a high byte. 
            >>> hex(a.HIGHBYTE(0x22))
            '0x2200'
            >>> hex(a.ADD(0xAABBCCDD, a.HIGHBYTE(0x22)))
            '0xaabbeedd'
"""


class AsmDec(object):

    def _get_size(self, value, size):
        """ return size based on register type """
        if type(value) == str:
            value = int(value.encode("hex"), 16)
        "l is for byte (8 bit) low byte registers: AL, BL, CL, DL"
        if size == "l":
            return value & 0xFF
        "h is for byte (8 bit) high byte registers: AH, BH, CH, DH"
        if size == "h":
            return (value & 0xFF00) >> 8
        "w is for word (16 bit) registers: AX, BX, CX, DX"
        if size == "w":
            return value & 0xFFFF
        "d is dword (32 bit) registerss: EAX, EBX, ECX, EDX, EBP, ESI, EDI, ESP"
        if size == "d":
            return value & 0xFFFFFFFF
        "q is qword (64 bit) registers: RAX, RBX, RCX, RDX, RDI, RDX, RDI, RSI, RBP, RSP, R8D-R15D, R8-R15"
        if size == "q":
            return value & 0xFFFFFFFFFFFFFFFF

    def _parse1(self, op1, size):
        """ return operand resized to match register type """
        size_op1 = size[0]
        temp_op1 = self._get_size(op1, size_op1)
        return temp_op1

    def _parse2(self, op1, op2, size):
        """ return operands resized to match register type  """
        size_op1 = size[0]
        size_op2 = size[1]
        temp_op1 = self._get_size(op1, size_op1)
        temp_op2 = self._get_size(op2, size_op2)
        return temp_op1, temp_op2

    def FORMAT(self, op1, size):
        """ format integer value """
        size_op1 = size[0]
        temp_op1 = self._get_size(op1, size_op1)
        return temp_op1

    def HIGHBYTE(self, value):
        return value << 8

    def XOR(self, op1, op2, size="dd"):
        """ Bitwise XOR """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 ^ op2, size[0])
        return temp

    def OR(self, op1, op2, size="dd"):
        """ Bitwise OR """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 | op2, size[0])
        return temp

    def AND(self, op1, op2, size="dd"):
        """ Bitwise AND """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 & op2, size[0])
        return temp

    def ROL(self, op1, op2, size="dd"):
        """ Bitwise rotate left  """
        # Credit:  Didier Stevens
        op1, op2 = self._parse2(op1, op2, size)
        temp = (op1 << op2 | op1 >> (8 - op2)) & 0xFF
        temp = self._get_size(temp, size[0])
        return temp

    def ROR(self, op1, op2, size="dd"):
        """ Bitwise rotate right """
        # Credit:  Didier Stevens
        op1, op2 = self._parse2(op1, op2, size)
        temp = (op1 >> op2 | op1 << (8- op2)) & 0xFF
        temp = self._get_size(temp, size[0])
        return temp

    def SHR(self, op1, op2, size="dd"):
        """ Shift operand right """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 >> op2, size[0])
        return temp

    def SHL(self, op1, op2, size="dd"):
        """ Shift operand left  """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 << op2, size[0])
        return temp

    def INC(self, op1, size="dd"):
        """ Increment operand """
        op1 = self._parse1(op1, size) + 1
        temp = self._get_size(op1, size[0])
        return temp

    def DEC(self, op1, size="dd"):
        """ Decrement operand """
        op1 = self._parse1(op1, size) - 1
        temp = self._get_size(op1, size[0])
        return temp

    def NEG(self, op1, size="dd"):
        """ Negate operand"""
        op1 = self._parse1(op1, size)
        temp = self._get_size( ~op1 + 1, size[0])
        return temp

    def NOT(self, op1, size="dd"):
        """ Not operand"""
        op1 = self._parse1(op1, size)
        temp = self._get_size( ~op1, size[0])
        return temp

    def ADD(self, op1, op2, size="dd"):
        """ Add operands """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 + op2, size[0])
        return temp

    def SUB(self, op1, op2, size="dd"):
        """ Subtract operands """
        op1, op2 = self._parse2(op1, op2, size)
        temp = self._get_size(op1 - op2, size[0])
        return temp

