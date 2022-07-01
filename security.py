"""
security.py

This module contains the functions for handling the encryption/decryption of data being stored in the database.

"""


import pickle, random
from globals import getValidChars


def generateKeyPattern():
    """
    Function to generate the sequence of integers used in modifying the characters in strings to be encrypted/decrypted.
    The sequence of integers is stored in a pickle file.
    
    No return value
    
    """
    
    sequence = tuple(random.randint(0, len(getValidChars())) for i in range(20))
    seq_file = open("seq.p", "wb")
    pickle.dump(sequence, seq_file)
    seq_file.close()

def encryptCharacter(character, offset):
    """
    Encrypts a character in a string by shifting its valid ascii bit value by the specified offset.
    If shifting by the offset exceeds the value allowed by ascii-valid characters, then decrease the value to "loop back" to the valid range of ascii characters.
    
    Returns the character after being encrypted
    
    """
    
    index = getValidChars().index(ord(character))
    if index + offset >= len(getValidChars()):
        return chr(getValidChars()[index + offset - len(getValidChars())])
    else:
        return chr(getValidChars()[index + offset])

def decryptCharacter(character, offset):
    """
    Decrypts a character in a string by shifting its valid ascii bit value by the specified offset.
    If shifting by the offset exceeds the value allowed by ascii-valid characters, then increase the value to "loop back" to the valid range of ascii characters.
    
    Returns the character after being decrypted
    
    """
    
    index = getValidChars().index(ord(character))
    if index - offset < 0:
        return chr(getValidChars()[index - offset + len(getValidChars())])
    else:
        return chr(getValidChars()[index - offset])

def encrypt(message):
    """
    Function to encrypt the specified message in preparation for storing it in the database
    
    Returns the encrypted string
    
    """
    
    try: # check if there is a pickle file that has stored the integer sequence used for encryption/decryption, otherwise we have to create one
        seq_file = open("seq.p", "rb")
        sequence = pickle.load(seq_file)
        seq_file.close()
    except FileNotFoundError: # there is no sequence stored, which means we need to create one
        generateKeyPattern()
        seq_file = open("seq.p", "rb")
        sequence = pickle.load(seq_file)
        seq_file.close()
    
    message_enc = "" # the encrypted message to be returned
    count = 0 # keeps track of which integer in the sequence to use as an offset
    
    # iterate through every character in the inputted message; we will encrypt each character by changing its unicode value by the given offset
    for c in message:
        offset = sequence[count % 20]
        message_enc += encryptCharacter(c, offset)
        count += 1
    
    return message_enc

def decrypt(message):
    """
    Function to decrypt the specified message
    
    Returns the decrypted string
    
    """
    
    # first, we read the sequence of integers stored in the pickle file back when we initiated encryption (this will never run before encryption has occurred)
    seq_file = open("seq.p", "rb")
    sequence = pickle.load(seq_file)
    seq_file.close()
    
    message_dec = "" # the decrypted message to be returned
    count = 0 # keeps track of which integer in the sequence to use as an offset
    
    # iterate through every character in the inputted message; we will decrypt each character by changing its unicode value by the given offset
    for c in message:
        offset = sequence[count % 20]
        message_dec += decryptCharacter(c, offset)
        count += 1
    
    return message_dec