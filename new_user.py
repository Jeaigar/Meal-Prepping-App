import sqlite3
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from subprocess import call
import argon2
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


# CHECKS THAT A VALID EMAIL HAS BEEN ENTERED
def check(email):

    if (re.fullmatch(regex, email)):
        return True

    else:
        return False


# TAKES THE USER BACK TO THE LOGIN SCREEN
# EXITS THE REGISTRATION WINDOW
def login():
    root.destroy()
    call(['python', 'login.py'])


# ALLOWS USER TO REGISTER THEIR NEW ACCOUNT
# CHECKS THAT USERNAME AND PASSWORD ENTRIES MEET CRITERIA
# IF PASSES ALL CHECKS, THE NEW ACCOUNT INFORMATION IS STORED IN THE DATABASE
def register():
    username = username_entry.get()
    password = password_entry.get()
    password_check = check_password_entry.get()
    email = email_entry.get()

    if (username == "" or username == "UserID") or (password == "" or password == "Password"):
        CTkMessagebox(title="Error", message="Please enter a username and password!", sound=True, icon="warning")

    elif password != password_check:
        CTkMessagebox(title="Error", message="Passwords do not match!", sound=True, icon="warning")

    elif not check(email):
        CTkMessagebox(title="Invalid Email", message="Please enter a valid email!", sound=True, icon="warning",)

    else:

        try:
            users = sqlite3.connect('login.db')
            mycursor = users.cursor()
            print("Connection established")

        except:
            messagebox.showerror("Connection Error", "Connection not established")

        try:

            command = ("create table users (user int auto_increment key not null,"
                       " Username varchar(255), Password varchar(255), Email varchar(319)")
            mycursor.execute(command)

        except:
            users = sqlite3.connect('login.db')
            mycursor = users.cursor()

            ph = argon2.PasswordHasher()
            ph.hash(password)
            hashed_password = ph.hash(password)

            command = "insert into users (Username, Password, Email) values (?, ?, ?)"

            mycursor.execute(command, (username, hashed_password, email))
            users.commit()
            users.close()
            messagebox.showinfo("Register", "New account has been created successfully!")

            login()


# IMPORTS THE LOGIN SCREEN LOGO
main_menu_logo = ctk.CTkImage(light_image=Image.open("main_menu_logo.png"),
                              dark_image=Image.open("main_menu_logo.png"), size=(200, 200))

# CREATES THE REGISTRATION WINDOW
root = ctk.CTk()
root.title("MealCraft")
root.geometry("400x600")  # Adjusted window size
root.iconbitmap(r"appicon.ico")
root.resizable(False, False)
root.eval("tk::PlaceWindow . center")

# CREATES AND PLACES THE APP LOGO
icon_label = ctk.CTkLabel(root, text="", height=180, width=50, image=main_menu_logo)
icon_label.place(x=100, y=20)

# CREATES AND PLACES THE "CREATE ACCOUNT" LABEL
# DISPLAYS "CREATE ACCOUNT"
title_label = ctk.CTkLabel(root, text="Create Account", font=("Helvetica", 30, "bold"))
title_label.place(x=90, y=225)

email_entry = ctk.CTkEntry(root, placeholder_text="Email", font=("Helvetica", 15, "bold"), width=220)
email_entry.place(x=90, y=270)

email_icon = ctk.CTkImage(Image.open('email_icon.png'))
email_icon._size = 25, 25

email_icon_label = ctk.CTkLabel(root, text="", font=("Helvetica", 15, "bold"), image=email_icon)
email_icon_label.place(x=60, y=270)


# CREATES AND PLACES AN ENTRY PROMPTING THE USER TO ENTER THEIR DESIRED USERNAME
username_entry = ctk.CTkEntry(root, placeholder_text="Username", font=("Helvetica", 15, "bold"), width=220)
username_entry.place(x=90, y=310)
username_entry.bind("<Key-space>", lambda e: "break")

user_icon = ctk.CTkImage(Image.open('name_icon.png'))
user_icon._size = 25, 25

user_icon_label = ctk.CTkLabel(root, text="", font=("Helvetica", 15, "bold"), image=user_icon)
user_icon_label.place(x=60, y=310)

# CREATES AND PLACES AN ENTRY PROMPTING THE USER TO ENTER THEIR PASSWORD
password_entry = ctk.CTkEntry(root, font=("Helvetica", 15, "bold"), width=220, placeholder_text="Password")
password_entry.place(x=90, y=350)
password_entry.bind("<Key-space>", lambda e: "break")

password_icon = ctk.CTkImage(Image.open('pass_icon.png'))
password_icon._size = 25, 25

password_icon_label = ctk.CTkLabel(root, text="", font=("Helvetica", 15, "bold"), image=password_icon)
password_icon_label.place(x=60, y=350)

# CREATES AND PLACES AN ENTRY TELLING THE USER TO REENTER THE PASSWORD THEY CHOSE
# ENSURING THAT BOTH PASSWORDS MATCH
check_password_entry = ctk.CTkEntry(root,
                                    font=("Helvetica", 15, "bold"), width=220, placeholder_text="Reenter password")
check_password_entry.place(x=90, y=390)
check_password_entry.bind("<Key-space>", lambda e: "break")

# CREATES AND PLACES A BUTTON THAT ALLOWS USERS TO COMPLETE THE ACCOUNT CREATION PROCESS
sign_up_button = ctk.CTkButton(root, text="Sign Up",
                               fg_color="#FF8433", hover_color="#FF6500", font=("Arial", 20, "bold"), command=register)
sign_up_button.place(x=129, y=440)

# CREATES AND PLACES A BUTTON THAT TAKES USERS BACK TO THE LOGIN SCREEN
login_button = ctk.CTkButton(root, text="Existing User?",
                             fg_color="#FF8433", hover_color="#FF6500", font=("Arial", 20, "bold"), command=login)
login_button.place(x=122, y=480)


root.mainloop()
