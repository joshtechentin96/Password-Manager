"""
register_screen.py

This module contains the functions for creating/maintaining the register new user screen, which is where we ask the user to enter a username and password for them to register to the program.

"""


import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from manage_passwords import passwordManagementScreen
from database_functions import registerNewUser
from globals import setUsername, isLoggedIn


def registerScreen():
    """
    Function for displaying the screen, allowing the user to enter their credentials in order to register for the program.
    
    If the user quits this window, it boots them back to the start screen.
    
    No return value
    
    """
    
    root = tk.Tk()
    root.title("Register")
    
    username_value = tk.StringVar()
    password_value = tk.StringVar()
    
    
    def register():
        """
        Internal function containing the logic for processing the user's inputted credentials, storing them in the database, and taking them to the password management screen.
        
        If the user didn't input a username, they will get an error message and get booted back to the register screen.
        If the user didn't input a password, they will get an error message and get booted back to the register screen.
        If the user entered a username that is already registered in the program, they will get an error message and get booted back to the register screen.
        
        No return value
        
        """
        
        username = username_value.get()
        if username == "":
            messagebox.showerror("Username Error", "You need to enter a username to register")
            return
        
        password = password_value.get()
        if password == "":
            messagebox.showerror("Password Error", "You need to enter a password to register")
            return
        elif "'" in password or '"' in password:
            messagebox.showerror("Password Error", "You cannot use single quotes or double quotes in your passwords.\nThese characters cause issues within the program.")
            return
        
        error_occurred = registerNewUser(username, password)
        if error_occurred:
            messagebox.showerror("Username Error", "That username has already been registered. Please select a different username.")
        else:
            setUsername(username)
            root.destroy()
            
            # loop the password management screen so that they keep getting brought back to it until they log out.
            while isLoggedIn():
                passwordManagementScreen()
    
    
    frame = ttk.Frame(root, padding = 10)
    frame.grid()
    
    info_label = ttk.Label(frame, text = "Select a username and a password")
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
    
    register_button = ttk.Button(frame, text = "Register", command = register)
    register_button.grid(column = 2, row = 5)
    
    root.mainloop()