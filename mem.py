#!/usr/bin/env python

class Memory():
    """
    Represents the state of main memory in for a program
    """
    pass

class Register():
    """
    Represents current the registers of a program 
    """

    @staticmethod
    def is_reg(s):
        """
        Returns True if s is the name of a valid register, else returns False
        """
        if s[0] == 'r':
            try:
                int(s[1:])
                return True
            except ValueError:
                return False
        return False
