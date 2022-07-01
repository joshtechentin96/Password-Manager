"""
random_password.py

This module contains a single function for generating random passwords for the user.

"""


import random
from globals import getValidChars


def generateRandomPassword():
    """
    Function for generating a random password.
    
    Returns a string that is a random combination of 20 letters, numbers, and symbols.
    This method ensures the randomly generated password has at least 1 number, 1 capital letter, 1 lowercase letter, and 1 symbol
    
    """
    
    random_password = ""
    while True:
        random_password = "".join(chr(random.choice(getValidChars())) for i in range(20))
        has_lower = has_upper = has_digit = has_symbol = False
        for c in random_password:
            if c.islower():
                has_lower = True
            elif c.isupper():
                has_upper = True
            elif c.isdigit():
                has_digit = True
            elif ord(c) < 48 or ord(c) > 122:
                has_symbol = True
                
            if has_lower and has_upper and has_digit and has_symbol:
                return random_password