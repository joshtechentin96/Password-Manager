"""
manage_passwords.py

This module contains the functions for creating/maintaining the manage passwords screen, which is the window in charge of:
    - Allowing the user to indicate they want to add new passwords
    - Allowing the user to indicate they want to change stored passwords
    - Allowing the user to indicate they want to delete stored passwords
    - Allowing the user to indicate they want to change their username/password
    - Allowing the user to see their stored passwords
    - Allowing the user to copy their stored passwords to their clipboard
    - Allowing the user to logout

"""


import pyperclip as pc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database_functions import getPasswordNames, getPassword, deletePassword
from add_new_password import addNewPasswordScreen
from edit_password import editPasswordScreen
from update_user_info import editProfileScreen
from globals import getUsername, setUsername, isLoggedIn


def passwordManagementScreen():
    """
    Function for displaying the password management screen, which is the primary control window for the program.
    
    No return value
    
    """
    
    
    class ManagementWindow(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)
            self.title("Password Manager")
            self.protocol("WM_DELETE_WINDOW", self.on_exit)
        def on_exit(self):
            self.destroy()
            setUsername("")
    
    
    root = ManagementWindow()
    
    
    class CopyButton(ttk.Button):
        def __init__(self, source, text_to_copy):
            self.text_to_copy = text_to_copy
            ttk.Button.__init__(self, source, text = "Copy", command = self.copyText)
        def copyText(self):
            pc.copy(self.text_to_copy)
    
    class ShowButton(ttk.Button):
        def __init__(self, source, heading_to_show, text_to_show):
            self.heading_to_show = heading_to_show
            self.text_to_show = text_to_show
            ttk.Button.__init__(self, source, text = "Show", command = self.showMessage)
        def showMessage(self):
            messagebox.showinfo(self.heading_to_show, self.text_to_show)
    
    class EditButton(ttk.Button):
        def __init__(self, source, password_name, password):
            self.password_name = password_name
            self.password = password
            ttk.Button.__init__(self, source, text = "Edit", command = self.editPassword)
        def editPassword(self):
            root.destroy()
            editPasswordScreen(self.password_name, self.password)
    
    class DeleteButton(ttk.Button):
        def __init__(self, source, password_name):
            self.password_name = password_name
            ttk.Button.__init__(self, source, text = "Delete", command = self.removePassword)
        def removePassword(self):
            root.destroy()
            deletePassword(getUsername(), self.password_name)
    
    def exitManager():
        root.destroy()
        setUsername("")
    
    def editProfile():
        root.destroy()
        editProfileScreen()
    
    def addNewPassword():
        root.destroy()
        addNewPasswordScreen()
    
    
    frame = ttk.Frame(root, padding = 10)
    frame.grid()
    
    main_label = ttk.Label(frame, text = "Password Names:")
    main_label.grid(column = 0, row = 0)
    
    ttk.Label(frame, text = "").grid(column = 0, row = 1)
    
    password_names = getPasswordNames(getUsername())
    passwords = [getPassword(getUsername(), password_name) for password_name in password_names]
    name_labels = []
    password_copy_buttons = []
    password_show_buttons = []
    password_edit_buttons = []
    
    row_num = 2
    if len(password_names) == 0:
        infoLabel = ttk.Label(frame, text = "No passwords registered yet")
        infoLabel.grid(column = 0, row = row_num)
        row_num += 1
    else:
        for password_name in password_names:
            name_labels.append(ttk.Label(frame, text = password_name).grid(column = 0, row = row_num))
            password_copy_buttons.append(CopyButton(frame, passwords[row_num - 2]))
            password_copy_buttons[row_num - 2].grid(column = 1, row = row_num)
            password_show_buttons.append(ShowButton(frame, password_names[row_num - 2], passwords[row_num - 2]))
            password_show_buttons[row_num - 2].grid(column = 2, row = row_num)
            password_edit_buttons.append(EditButton(frame, password_names[row_num - 2], passwords[row_num - 2]))
            password_edit_buttons[row_num - 2].grid(column = 3, row = row_num)
            row_num += 1
    
    ttk.Label(frame, text = "").grid(column = 0, row = row_num)
    row_num += 1
    
    logout_button = ttk.Button(frame, text = "Logout", command = exitManager)
    logout_button.grid(column = 1, row = row_num)
    
    edit_button = ttk.Button(frame, text = "Edit profile", command = editProfile)
    edit_button.grid(column = 2, row = row_num)
    
    add_button = ttk.Button(frame, text = "Add New Password", command = addNewPassword)
    add_button.grid(column = 3, row = row_num)
    
    root.mainloop()