"""
start_screen.py

This module contains the functions for creating/maintaining the start screen, which is where the user can quit the program, choose to register, or choose to login.

"""


import os
import tkinter as tk
from tkinter import ttk
from register_screen import registerScreen
from login_screen import loginScreen
from database_functions import getNumUsers


def startScreen():
    """
    Function for displaying the first screen in the program, which gives the user an option to either login or register to the program.
    
    No return value.
    
    """
    
    class StartWindow(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            self.title("Password Manager")
            self.protocol("WM_DELETE_WINDOW", self.on_exit)
        def on_exit(self):
            self.destroy()
            os._exit(0)
    
    
    root = StartWindow()
    
    
    def register():
        """
        Internal function to call the main function for creating the registration screen.
        
        This function is called whenever the user pushes the "Register New User" button on the start screen.
        
        No return value.
        
        """
        
        root.destroy()
        registerScreen()
    
    def login():
        """
        Internal function to call the main funtion for creating the login screen.
        
        This function is called whenever the user pushes the "Login" button on the start screen.
        
        No return value.
        
        """
        
        root.destroy()
        loginScreen()
    
        
    frame = ttk.Frame(root, padding = 10)
    frame.grid()
    
    welcome_label = ttk.Label(frame, text = "Welcome to the Password Manager!")
    welcome_label.grid(column = 1, row = 0)
    
    new_user_label = ttk.Label(frame, text = "If you are a new user, click the \"Register New User\" button")
    new_user_label.grid(column = 1, row = 1)
    
    login_label = ttk.Label(frame, text = "If you have already registered, click the \"Login\" button")
    login_label.grid(column = 1, row = 2)
    
    ttk.Label(frame, text = "").grid(column = 0, row = 3)
    
    quit_button = ttk.Button(frame, text = "Quit", command = root.on_exit)
    quit_button.grid(column = 0, row = 4)
    
    register_button = ttk.Button(frame, text = "Register New User", command = register)
    register_button.grid(column = 1, row = 4)
    
    login_button = ttk.Button(frame, text = "Login", command = login)
    login_button.grid(column = 2, row = 4)
    
    # disable the login button if no users have been registered yet
    num_users = getNumUsers()
    
    if num_users == 0:
        login_button["state"] = tk.DISABLED
    
    root.mainloop()