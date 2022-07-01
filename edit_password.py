"""
edit_password.py

This module contains the functions for creating/maintaining the edit password screen, which allows users to change their stored passwords.

"""


import tkinter as tk
from tkinter import ttk
from database_functions import updatePassword
from random_password import generateRandomPassword
from globals import getUsername


def editPasswordScreen(password_name, password):
    """
    Function for displaying the edit password screen, allowing the user to modify their stored passwords.
    
    No return value
    
    """
    
    root = tk.Tk()
    root.title("Edit Password")
    
    new_password_value = tk.StringVar()
    
    
    def getRandomPassword():
        new_password_value.set(generateRandomPassword())
    
    def editPassword():
        updatePassword(getUsername(), password_name, new_password_value.get())
        root.destroy()
    
    
    frame = ttk.Frame(root, padding = 10)
    frame.grid()
    
    password_name_label = ttk.Label(frame, text = password_name)
    password_name_label.grid(column = 0, row = 0)
    
    current_password_label = ttk.Label(frame, text = "The password is currently: " + password)
    current_password_label.grid(column = 0, row = 1)
    
    new_password_label = ttk.Label(frame, text = "Enter a new password and click \"Confirm\"")
    new_password_label.grid(column = 0, row = 2)
    
    new_password_entry = ttk.Entry(frame, textvariable = new_password_value, show = "*")
    new_password_entry.grid(column = 1, row = 2)
    
    random_password_button = ttk.Button(frame, text = "Generate Random Password", command = getRandomPassword)
    random_password_button.grid(column = 1, row = 1)
    
    ttk.Label(frame, text = "").grid(column = 0, row = 3)
    
    cancel_button = ttk.Button(frame, text = "Cancel", command = root.destroy)
    cancel_button.grid(column = 0, row = 4)
    
    confirm_button = ttk.Button(frame, text = "Confirm", command = editPassword)
    confirm_button.grid(column = 1, row = 4)
    
    root.mainloop()