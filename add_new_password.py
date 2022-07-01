"""
add_new_password.py

This module contains the functions for creating/maintaining the add_new_password screen, which is where users can add a new password they wish to store in this program.

"""


import tkinter as tk
from tkinter import ttk
from database_functions import storePassword
from random_password import generateRandomPassword
from globals import getUsername


def addNewPasswordScreen():
    """
    Function for displaying the add new password screen, allowing the user to add a specified new password to be stored in the program.
    
    No return value
    
    """
    
    root = tk.Tk()
    root.title("Add New Password")

    password_name_value = tk.StringVar()
    password_value = tk.StringVar()


    def getRandomPassword():        
        password_value.set(generateRandomPassword())
    
    def addPassword():
        password_name = password_name_value.get()
        password = password_value.get()
        storePassword(getUsername(), password_name, password)
        root.destroy()


    frame = ttk.Frame(root, padding = 10)
    frame.grid()

    password_name_label = ttk.Label(frame, text = "Enter the name of the password:")
    password_name_label.grid(column = 1, row = 0)
    
    ttk.Label(frame, text = "(e.g. Bank Password, Computer Password, etc.)").grid(column = 1, row = 1)
    
    password_name_entry = ttk.Entry(frame, textvariable = password_name_value)
    password_name_entry.grid(column = 1, row = 2)
    
    ttk.Label(frame, text = "").grid(column = 1, row = 3)
    
    password_label = ttk.Label(frame, text = "Enter the password:")
    password_label.grid(column = 1, row = 4)
    
    password_entry = ttk.Entry(frame, textvariable = password_value, show = "*")
    password_entry.grid(column = 1, row = 5)
    
    random_button = ttk.Button(frame, text = "Generate Random Password", command = getRandomPassword)
    random_button.grid(column = 1, row = 6)
    
    ttk.Label(frame, text = "").grid(column = 1, row = 7)
    
    back_button = ttk.Button(frame, text = "Back", command = root.destroy)
    back_button.grid(column = 0, row = 8)
    
    confirm_button = ttk.Button(frame, text = "Confirm", command = addPassword)
    confirm_button.grid(column = 2, row = 8)

    root.mainloop()