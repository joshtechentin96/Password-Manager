"""
globals.py

This modules contains global variables and the functions needed to access/modify them.

"""

username = "" # the username of the user who is currently logged in; it is an empty string if no one is logged in
valid_password_chars = tuple(range(32, 34)) + tuple(range(35, 39)) + tuple(range(40, 127)) # the ascii values of all valid characters that can be used in password (excludes ', ", and non-typeable characters)

def getUsername():
    return username

def setUsername(newName):
    global username
    username = newName

def isLoggedIn():
    return username != ""

def getValidChars():
    return valid_password_chars