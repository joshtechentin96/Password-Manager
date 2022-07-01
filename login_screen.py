"""
login_screen.py

This module contains the functions used for creating/maintaining the login screen, which is where we ask users for their credentials so they can login to the program they have already registered for.

"""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from manage_passwords import passwordManagementScreen
from database_functions import loginUser
from globals import setUsername, isLoggedIn


def loginScreen():
    """
    Function for displaying the login screen, allowing the user to input their credentials and login to the program if they have already registered.
    
    If the user quits this window, it boots them back to the start screen.
    
    No return value
    
    """
    
    root = tk.Tk()
    
    username_value = tk.StringVar()
    password_value = tk.StringVar()
    
    
    def login():
        """
        Internal function containing the logic for processing the user's inputted credentials and taking them to the password management screen.
        
        If the user inputted a username not stored in the database, they will get an error message and get booted back to the login screen.
        If the user entered the wrong password, they will get an error message and get booted back to the login screen.
        
        No return value
        
        """
        
        username = username_value.get()
        password = password_value.get()
        if "'" in password or '"' in password:
            messagebox.showerror("Password Error", "The password is incorrect.")
            return
        
        error_number = loginUser(username, password)
        if error_number == 1:
            messagebox.showerror("Username Error", "That username has not been registered.\nYour username is either misspelled or you need to register as a new user.")
        elif error_number == 2:
            messagebox.showerror("Password Error", "The password is incorrect.")
        else:
            setUsername(username)
            root.destroy()
            
            # loop the password management screen so that they keep getting brought back to it until they log out.
            while isLoggedIn():
                passwordManagementScreen()
    
    
    frame = ttk.Frame(root, padding = 10)
    frame.grid()
    
    info_label = ttk.Label(frame, text = "Enter your username and password")
    info_label.grid(column = 1, row = 0)
    
    ttk.Label(frame, text = "").grid(column = 0, row = 1)
    
    username_label = ttk.Label(frame, text = "Username:")
    username_label.grid(column = 0, row = 2)
    
    username_entry = ttk.Entry(frame, textvariable = username_value)
    username_entry.grid(column = 2, row = 2)
    
    password_label = ttk.Label(frame, text = "Password:")
    password_label.grid(column = 0, row = 3)
    
    password_entry = ttk.Entry(frame, textvariable = password_value, show = "*")
    password_entry.grid(column = 2, row = 3)
    
    ttk.Label(frame, text = "").grid(column = 0, row = 4)
    
    back_button = ttk.Button(frame, text = "Back", command = root.destroy)
    back_button.grid(column = 0, row = 5)
    
    login_button = ttk.Button(frame, text = "Login", command = login)
    login_button.grid(column = 2, row = 5)
    
    root.mainloop()