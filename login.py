from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import tkinter as tk
from subprocess import call
from tkinter import messagebox
import argon2
import sqlite3

if __name__ == '__main__':
    current_user = None


    # REMOVES "PASSWORD" IN PASSWORD ENTRY
    def password_enter(e):
        password_entry.delete(0,'end')


    # INSERTS "PASSWORD" INTO ENTRY BY DEFAULT
    def password_leave(e):
        if password_entry.get() == '':
            password_entry.insert(0,'Password')


    # SENDS USER TO THE ACCOUNT CREATION SCREEN
    # EXITS CURRENT WINDOW AND OPENS A DIFFERENT ONE
    def register():
        login.destroy()
        call(['python', 'new_user.py'])


    # ADDS FUNCTIONALITY TO THE "EYE BUTTON"
    # IMPLEMENTS THE ABILITY TO HIDE PASSWORD WHEN BUTTON IS CLICKED
    def hide():
        global button_mode
        if button_mode:
            eye_button.configure(image=closedeye, activebackground="white")
            password_entry.configure(show="*")
            button_mode = False
        else:
            eye_button.configure(image=openeye, activebackground="white")
            password_entry.configure(show="")
            button_mode = True


    # ALLOWS USER TO LOGIN TO THE APP
    # GETS ENTERED USERNAME AND PASSWORD AND CHECKS IF THEY MEET CRITERIA
    # IF THEY MEET THE REQUIREMENTS, THE APP CONNECTS TO THE DATABASE AND SEARCHES FOR A MATCHING USERNAME AND PASSWORD
    # IF A MATCHING USERNAME AND PASSWORD ARE NOT FOUND, IT WILL NOT ALLOW YOU TO LOGIN
    # IF A MATCHING USERNAME AND PASSWORD ARE FOUND, THE APP WILL ALLOW USER TO SUCCESSFULLY LOGIN

    # RETURNS ENCRYPTED PASSWORD FROM DATABASE AND COMPARES IT TO THE PASSWORD ENTERED (BOOL)
    # IF TRUE , THE LOGIN IS SUCCESSFUL
    # IF FALSE, THE USER IS PROMPTED WITH "INVALID USERNAME OR PASSWORD"
    def loginuser(event):
        username = username_entry.get()
        password = password_entry.get()

        if (username == "" or username == "Username") or (password == "" or password == "Password"):
            CTkMessagebox(title="Error", message="Enter a valid username and password!", icon='warning', sound=True)

        else:

            try:
                users = sqlite3.connect('login.db')
                mycursor = users.cursor()
                print("Connected to database!")

            except:
                CTkMessagebox(title="Error", message="Database connection not established!", icon='warning')
                return

            ph = argon2.PasswordHasher()

            command = "select * from users where Username = ?"
            mycursor.execute(command, (username,))

            myresult = mycursor.fetchone()

            # FOR DEBUG
            # print(myresult)
            # print(f'Password : {fetched_password}')

            if myresult is None:

                CTkMessagebox(title="Error", message="Username doesn't exist!", icon='warning', sound=True)

            else:
                try:
                    fetched_password = myresult[2]
                    ph.verify(fetched_password, password)
                    print('Password verified!')
                    current_user = username
                    print(current_user)
                    messagebox.showinfo("Login", "Login successful!")

                    login.destroy()

                    call(['python', 'main.py'])

                except:
                    CTkMessagebox(title="Error", message="Invalid username or password!", icon='warning', sound=True)
                    print('Password verification failed!')


    # ADDS SHARPNESS TO UI ON HIGH-RESOLUTION SCREENS
    def enable_high_dpi_awareness():
        try:

            login.tk.call('tk', 'scaling', 2.0)

        except:
            pass


    # IMPORTS THE LOGIN SCREEN LOGO
    main_menu_logo = ctk.CTkImage(light_image=Image.open("main_menu_logo.png"), dark_image=Image.open("main_menu_logo.png"), size=(200, 200))

    # Create the main window
    login = ctk.CTk()
    login.title("MealCraft")
    login.geometry("400x500")
    login.iconbitmap(r"appicon.ico")
    login.resizable(False, False)
    login.eval("tk::PlaceWindow . center")

    # Enable DPI scaling
    enable_high_dpi_awareness()


    # Set dark mode
    ctk.set_appearance_mode("dark")

    # CREATES AND PLACES THE LABEL THAT HOUSES THE LOGIN SCREEN LOGO
    icon_label = ctk.CTkLabel(login, text="", height=180, width=50, image=main_menu_logo)
    icon_label.place(x=100, y=20)

    # CREATES AND PLACES THE ENTRY FOR USERS TO ENTER THEIR USERNAME
    username_entry = ctk.CTkEntry(login, placeholder_text="Username", font=("Arial", 15, "bold"), placeholder_text_color="white", width=200)
    username_entry.bind("<Key-space>", lambda e: "break")
    username_entry.place(x=100, y=255)


    # IMPORTS THE USERNAME ICON
    name_icon = ctk.CTkImage(Image.open('name_icon.png'))
    name_icon._size = 25, 25

    # CREATES AND PLACES USERNAME ICON LABEL
    name_icon_label = ctk.CTkLabel(login, image=name_icon, text='')
    name_icon_label.place(x=70, y=255)

    # CREATES AND PLACES THE ENTRY FOR USERS TO ENTER THEIR PASSWORD
    password_entry = ctk.CTkEntry(login, font=("Arial", 15, "bold"), width=200)
    password_entry.insert(0, 'Password')
    password_entry.bind("<FocusIn>", password_enter)
    password_entry.bind("<FocusOut>", password_leave)
    password_entry.bind("<Key-space>", lambda e: "break")
    password_entry.place(x=100, y=290)

    # ALLOWS USER TO PRESS ENTER BUTTON TO LOGIN
    login.bind("<Return>", loginuser)


    # IMPORTS THE PASSWORD ICON
    pass_icon = ctk.CTkImage(Image.open('pass_icon.png'))
    pass_icon._size = 25, 25

    # CREATES AND PLACES USERNAME ICON LABEL
    pass_icon_label = ctk.CTkLabel(login, image=pass_icon, text='')
    pass_icon_label.place(x=71, y=290)

    # IMPORTS THE OPEN EYE BUTTON TO PASSWORD ENTRY
    openeye = Image.open("openeye.png")
    openeye = openeye.resize((18, 14))
    openeye = ImageTk.PhotoImage(openeye)

    # IMPORTS THE CLOSED EYE BUTTON TO PASSWORD ENTRY
    closedeye = Image.open("closedeye.png")
    closedeye = closedeye.resize((18,12))
    closedeye = ImageTk.PhotoImage(closedeye)

    button_mode = True

    # CREATES AND PLACES THE OPEN/CLOSED EYE BUTTON FOR PASSWORD ENTRY
    eye_button = tk.Button(login, image=openeye, bd=0,bg="#343434", command=hide)
    eye_button.place(x=260, y=297)

    # CREATES AND PLACES THE "REMEMBER ME" CHECKBOX
    remember_me = ctk.CTkCheckBox(login, text="Remember Me", font=("Arial", 15), checkmark_color="white", fg_color="#FF8433", hover_color="#FF6500")
    remember_me.place(x=100, y=335)

    # CREATES AND PLACES THE LOGIN BUTTON
    login_button = ctk.CTkButton(login, text="Login", font=("Arial", 20), fg_color="#FF8433", hover_color="#FF6500", command= lambda: loginuser(None))
    login_button.place(x=129, y=380)

    # CREATES AND PLACES THE REGISTER BUTTON
    register_button = ctk.CTkButton(login, text="Register", font=("Arial", 20), fg_color="#FF8433", hover_color="#FF6500", command=register)
    register_button.place(x=129, y=420)


    login.mainloop()
