"""
database_functions.py

This module contains the functions used for communicating with the SQL database.

"""


import sqlite3 as sql
from security import encrypt, decrypt


def getNumUsers():
    """
    Function to fetch all of the usernames stored in the database.
    
    Return value will be an integer of the number of usernames stored in the database
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure a table has been created for users in the database; if not return 0
    cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = 'users';")
    if cur.fetchone()[0] == 0:
        conn.close()
        return 0
    
    cur.execute("SELECT DISTINCT username FROM users;")
    usernames = cur.fetchall()
    
    conn.close()
    
    return len(usernames)

def loginUser(username, password):
    """
    Function to log the user into the password manager.
    
    Return value will be an integer as follows:
    
    0 if the user is logged in with no issues
    1 if the specified username has not been registered with the password manager
    2 if the specified username has been registered with the password manager, but the password is incorrect
    """
    
    username_enc = encrypt(username)
    password_enc = encrypt(password)
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure a table has been created for users in the database
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'users';")
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE TABLE users (username TEXT, password TEXT);")
        conn.commit()
        conn.close()
        return 1 # if no table has been created, obviously the username hasn't been stored yet
    
    # ensure the user has already been registered
    cur.execute("SELECT COUNT(*) FROM users WHERE username = '" + username_enc + "';")
    if cur.fetchone()[0] == 0:
        conn.close()
        return 1
    
    # ensure the specified password is correct
    cur.execute("SELECT COUNT(*) FROM users WHERE username = '" + username_enc + "' AND password = '" + password_enc + "';")
    if cur.fetchone()[0] == 0:
        conn.close()
        return 2
    
    conn.close()
    
    return 0
    
def registerNewUser(username, password):
    """
    Function to register a new user to the program, with the specified username and password.
    
    Return value will be an integer as follows:
    
    0 if the user is registered with no issues
    1 if the username specified cannot be used as a user is already registered with that username
    
    """
    
    username_enc = encrypt(username)
    password_enc = encrypt(password)
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure a table has been created for users in the database
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table' AND name = 'users';")
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE TABLE users (username TEXT, password TEXT);")
        conn.commit()
    
    # ensure no other user has been registered with the same username
    cur.execute("SELECT COUNT(*) FROM users WHERE username = '" + username_enc + "';")
    if cur.fetchone()[0] > 0:
        conn.close()
        return 1
        
    cur.execute("INSERT INTO users (username, password) VALUES ('" + username_enc + "', '" + password_enc + "');")
    
    conn.commit()
    conn.close()
    
    return 0

def updateUsername(old_username, new_username):
    """
    Function to update the current user's username.
    
    old_username is the user's current username.
    new_username is the user's requested new username.
    
    Return value will be an integer as follows:
    
    0 if the user's credentials are updated with no issue
    1 if the user's newly selected username already exists in the database
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure no other has been registered with the same username
    cur.execute("SELECT COUNT(*) FROM users WHERE username = '" + encrypt(new_username) + "';")
    if cur.fetchone()[0] > 0:
        conn.close()
        return 1
    
    new_username_enc = encrypt(new_username)
    old_username_enc = encrypt(old_username)
    
    cur.execute("UPDATE users SET username = '" + new_username_enc + "' WHERE username = '" + old_username_enc + "';")
    cur.execute("UPDATE user_passwords SET username = '" + encrypt(new_username) + "' WHERE username = '" + old_username_enc + "';")
    
    conn.commit()
    conn.close()
    
    return 0

def updateLoginPassword(username, new_password):
    """
    Function for updating the specified user's main password for this program.
    
    No return value
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    cur.execute("UPDATE users SET password = '" + encrypt(new_password) + "' WHERE username = '" + encrypt(username) + "';")
    
    conn.commit()
    conn.close()

def getPasswordNames(username):
    """
    Function for fetching all of the various password names the specified user has stored in the database (e.g. "Bank password", "School password", etc.)
    
    Returns a list with all of the password names (each password is a single valued tuple)
    An empty list will be returned if no passwords have been stored
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure table has been created for storing user passwords
    cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = 'user_passwords';")
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE TABLE user_passwords (username TEXT, password_name TEXT, password TEXT);")
        conn.commit()
        conn.close()
        return [] # if no table had been created, naturally no passwords have been stored
    
    cur.execute("SELECT password_name FROM user_passwords WHERE username = '" + encrypt(username) + "';")
    password_names = [decrypt(password_name[0]) for password_name in cur.fetchall()]
    
    conn.close()
    
    return password_names

def getPassword(username, password_name):
    """
    Function to fetch the specified user's password with the specified password_name
    
    Returns a string value equal to the stored password with name password_name
    Returns a null string if no password exists with the specified password_name
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure table has been created for storing user passwords
    cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = 'user_passwords';")
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE TABLE user_passwords (username TEXT, password_name TEXT, password TEXT);")
        conn.commit()
        return "" # if no table had been created, naturally no passwords have been stored
    
    cur.execute("SELECT password FROM user_passwords WHERE username = '" + encrypt(username) + "' AND password_name = '" + encrypt(password_name) + "';")
    password = decrypt(cur.fetchone()[0])
    
    conn.close()
    
    return password

def storePassword(username, password_name, password):
    """
    Function to store the specified user's specified password with specified password_name
    
    No return value
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    # ensure table has been created for storing user passwords
    cur.execute("SELECT COUNT(name) FROM sqlite_master WHERE type = 'table' AND name = 'user_passwords';")
    if cur.fetchone()[0] == 0:
        cur.execute("CREATE TABLE user_passwords (username TEXT, password_name TEXT, password TEXT);")
        conn.commit()
    
    cur.execute("INSERT INTO user_passwords (username, password_name, password) VALUES ('" + encrypt(username) + "', '" + encrypt(password_name) + "', '" + encrypt(password) + "');")
    conn.commit()
    
    conn.close()

def deletePassword(username, password_name):
    """
    Function to delete the specified user's specified password from the database
    
    No return value
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    
    cur.execute("DELETE FROM user_passwords WHERE username = '" + encrypt(username) + "' AND password_name = '" + encrypt(password_name) + "';")
    
    conn.commit()
    conn.close()

def updatePassword(username, password_name, new_password):
    """
    Function for updating the specified user's password of name password_name to value new_password.
    
    No return value
    
    """
    
    conn = sql.connect("data.db")
    cur = conn.cursor()
    try:
        cur.execute("UPDATE user_passwords SET password = '" + encrypt(new_password) + "' WHERE username = '" + encrypt(username) + "' AND password_name = '" + encrypt(password_name) + "';")
    except:
        print("Problem with updating password to " +  new_password + " and encrypting to " + encrypt(new_password))
    
    conn.commit()
    conn.close()