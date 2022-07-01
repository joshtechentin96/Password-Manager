"""
update_user_info.py

This module contains the functions for creating/maintaining the update user info screen, which allows users to change their username/password.

"""


import tkinter as tk
from tkinter import ttk
from database_functions import updateUsername, updateLoginPassword
from globals import getUsername, setUsername


def editProfileScreen():
    """
    Function for displaying the edit profile screen, allowing the user to change their username/password.
    
    No return value
    
    """
    
    root = tk.Tk()
    
    user_check_value = tk.IntVar()
    pass_check_value = tk.IntVar()
    
    username_value = tk.StringVar()
    password_value = tk.StringVar()
    
    
    def updateProfile():
        ignore_username = user_check_value.get()
        ignore_password = pass_check_value.get()
        
        new_name = username_value.get()
        new_password = password_value.get()
        
        # we need to check for potential errors before updating anything in the database, otherwise we could end up updating a username but not the password, messing things up
        if not ignore_username and new_name == "":
            tk.messagebox.showerror("Username Error", "Username cannot be blank.")
            return
        
        if not ignore_password and new_password == "":
            tk.messagebox.showerror("Password Error", "Password cannot be blank.")
            return
        
        if "'" in new_password or '"' in new_password:
            tk.messagebox.showerror("Password Error", "You cannot use single quotes or double quotes in your passwords.\nThese characters cause issues within the program.")
            return
        
        if not ignore_username:
            error_occurred = updateUsername(getUsername(), new_name)
            if error_occurred:
                tk.messagebox.showerror("Username Error", "That username has already been registered. Please select a different username.")
                return
            else:
                setUsername(new_name)
        
        if not ignore_password:
            updateLoginPassword(getUsername(), new_password)
        
        tk.messagebox.showinfo("Success", "Your requested info has been updated.")
        root.destroy()
    
    
    frame = ttk.Frame(root, padding = 10)
    frame.grid()
    
    username_label = ttk.Label(frame, text = "New username:")
    username_label.grid(column = 1, row = 0)
    
    username_entry = ttk.Entry(frame, textvariable = username_value)
    username_entry.grid(column = 1, row = 1)
    
    username_check = ttk.Checkbutton(frame, text = "I don't want to update my username", variable = user_check_value, onvalue = 1, offvalue = 0)
    username_check.grid(column = 1, row = 2)
    
    ttk.Label(frame, text = "").grid(column = 1, row = 3)
    
    password_label = ttk.Label(frame, text = "New password:")
    password_label.grid(column = 1, row = 4)
    
    password_entry = ttk.Entry(frame, textvariable = password_value, show = "*")
    password_entry.grid(column = 1, row = 5)
    
    password_check = ttk.Checkbutton(frame, text = "I don't want to update my password", variable = pass_check_value, onvalue = 1, offvalue = 0)
    password_check.grid(column = 1, row = 6)
    
    ttk.Label(frame, text = "").grid(column = 1, row = 7)
    
    back_button = ttk.Button(frame, text = "Cancel", command = root.destroy)
    back_button.grid(column = 0, row = 8)
    
    confirm_button = ttk.Button(frame, text = "Confirm", command = updateProfile)
    confirm_button.grid(column = 2, row = 8)
    
    root.mainloop()