from tkinter import messagebox
from subprocess import call
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import random
from customtkinter import CTkButton
from PIL import Image, ImageTk
import openai
import sqlite3



def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def exit_button(window):

    users = sqlite3.connect('login.db')
    mycursor = users.cursor()

    command = "update users set LoggedIn = 0 where LoggedIn = 1"
    mycursor.execute(command)
    users.commit()
    users.close()

    window.destroy()


def logout():

    users = sqlite3.connect('login.db')
    mycursor = users.cursor()

    command = "update users set LoggedIn = 0 where LoggedIn = 1"
    mycursor.execute(command)
    users.commit()
    users.close()

    messagebox.showinfo("Logout", "Logging out...")

    run.destroy()

    call(["python", "login.py"])


# Set dark mode
ctk.set_appearance_mode("dark")


class Main(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.wm_title('MealCraft')
        self.geometry('1000x600')
        self._set_appearance_mode('dark')
        self.resizable(False, False)
        self.wm_iconbitmap('appicon.ico')
        self.eval("tk::PlaceWindow . center")
        self.protocol("WM_DELETE_WINDOW", lambda: exit_button(self))

        self.bg = Image.open('main_bg.png')
        self.bg = ctk.CTkImage(self.bg, size=(1000, 600))

        bg_label = ctk.CTkLabel(self, image=self.bg)
        bg_label.place(x=0, y=0)


        # CONNECTS TO DATABASE
        users = sqlite3.connect('login.db')
        mycursor = users.cursor()

        # FINDS THE USER THAT IS CURRENTLY LOGGED IN
        command = "select * from users where LoggedIn = 1"
        mycursor.execute(command)

        # GETS THE CURRENTLY LOGGED IN USER INFO
        result = mycursor.fetchone()

        # GETS THE CURRENTLY LOGGED IN USER AND ASSIGNS IT TO "logged_in_user" VARIABLE
        # logged_in_user = result[1]

        # CREATES AND PLACES FRAME FOR WIDGETS ON THE RIGHT SIDE
        container = ctk.CTkFrame(self, height=550, width=710)
        container.place(x=270, y=25)

        self.frames = {}

        for F in (AIPage, SummaryPage, PlanPage, CalcPage):
            frame = F(container, self)
            frame.configure(height=550, width=710, bg_color='#232323', fg_color='#2B2B2B')

            self.frames[F] = frame
            frame.place(x=0, y=0)

        self.show_frames(SummaryPage)

        # CREATES TOOLBAR THAT HOLDS MAIN PAGE BUTTONS, NAME LABEL, AND PROFILE PICTURE
        toolbar = ctk.CTkFrame(self, height=500, width=200)
        toolbar.place(x=25, y=50)

        # OPENS PROFILE PICTURE AND DISPLAYS IT IN THE TOOLBAR
        account_icon = ctk.CTkImage(Image.open("account_icon.png"))
        account_icon._size = 150, 100
        account_icon_label = ctk.CTkLabel(toolbar, image=account_icon, text='')
        account_icon_label.place(anchor='nw', y=20, x=25)

        # BUTTON THAT ALLOWS USER TO SIGN OUT OF THEIR ACCOUNT
        sign_out = CTkButton(toolbar, text="Sign Out", command=logout, height=30, width=20,
                             fg_color='dark red', hover_color= 'green',
                             font=("Arial", 12, 'bold'))
        sign_out.place(anchor='nw', y=170, x=70)

        # LABEL THAT SHOWS THE CURRENTLY LOGGED IN USER
        name_label = ctk.CTkLabel(toolbar, text='logged_in_user', font=("Helvetica", 23, 'bold'), width=200)
        name_label.place(anchor='sw', y=160, x=0)

        # SHOWS AN OVERVIEW OF THE USERS MEALS
        summary_button = ctk.CTkButton(toolbar, command=lambda: self.show_frames(SummaryPage), text="Summary",
                                       font=('Helvetica', 20, 'bold'), fg_color="#FF8433", hover_color="#FF6500")
        summary_button.place(anchor='nw', y=225, x=30)

        # TAKES USERS TO MEAL PLAN PAGE
        plan_meal_button = ctk.CTkButton(toolbar, command=lambda: self.show_frames(PlanPage), text="Plan Your Meal",
                                         font=('Helvetica', 15, 'bold'), fg_color="#FF8433", hover_color="#FF6500")
        plan_meal_button.place(anchor='nw', y=275, x=30)

        # OPENS PROMPT FOR USERS TO ASK AI FOR MEAL SUGGESTIONS
        ask_button = ctk.CTkButton(toolbar, command=lambda: self.show_frames(AIPage), text="Not sure? Ask AI",
                                   font=('Helvetica', 15, 'bold'), fg_color="#FF8433", hover_color="#FF6500")
        ask_button.place(anchor='nw', y=325, x=30)

        # CREATES AND PLACES SEPARATOR BETWEEN TOOL BAR ON THE LEFT SIDE AND THE RIGHT SIDE
        # sep_frame = ctk.CTkFrame(self, height=500, width=1)
        # sep_frame.place(x=250, y=50)

    # FUNCTION THAT RAISES FRAMES (OPENS NEW FRAME WHEN BUTTON IS PRESSED)
    def show_frames(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SummaryPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        button = ctk.CTkButton(self, text='Summary', command=lambda: controller.show_frames(CalcPage))
        button.place(x=50, y=50)


class AIPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        def ai_chat(prompt):
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt},
                          {"role": "assistant", "content": "Ask more questions"},
                          {"role": "assistant", "content": "Be less formal."},
                          {"role": "assistant", "content": "Respond with 20 words or less."},
                          {"role": "assistant", "content": "You are a professional nutritionist"},],
                temperature=0.8,
                max_tokens=200,
                frequency_penalty=0.5,
                presence_penalty=0.5,

            )

            return response.choices[0].message.content.strip()

        def ask_ai(user, label):
            response = ai_chat(user)
            label.configure(text=response)
            user_entry_box.delete(0, 'end')

        API_KEY = open("API_KEY.txt", 'r').read()
        openai.api_key = API_KEY

        response_label = ctk.CTkLabel(self, text='', bg_color='dark gray', height=300, width=600)
        response_label.place(x=50, y=30)

        user_entry_box = ctk.CTkEntry(self, height=100, width=500, font=("Arial", 40, 'bold'))
        user_entry_box.place(x=50, y=400)

        ask_button = ctk.CTkButton(self, text='Ask AI',
                                   fg_color="#FF8433", hover_color="#FF6500",
                                   height=30, width=300, font=("Arial", 20, 'bold'),
                                   command=lambda: ask_ai(user_entry_box.get(), response_label))
        ask_button.place(x=50, y=500)


class PlanPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        # Food, sides, and drinks corresponding to each diet
        food_options = {
            "None": ["Pizza", "Burger", "Burrito"],
            "Vegetarian": ["Grilled Vegetables", "Vegetable Stir Fry",
                           "Lentil Soup", "Vegetarian Lasagna", "Falafel", "Veggie Burger", "Eggplant Parmesan"],
            "Vegan": ["Vegan Pasta", "Tofu Salad", "Chickpea Curry"],
            "Keto": ["Grilled Chicken", "Salmon", "Avocado Salad"],
            "Paleo": ["Steak", "Sweet Potato", "Chicken Salad"]
        }

        side_options = {
            "None": ["Fries", "Onion Rings", "Garlic Bread"],
            "Vegetarian": ["Fruit Salad", "Hummus", "Cheese Sticks"],
            "Vegan": ["Veggie Chips", "Hummus", "Apple Slices"],
            "Keto": ["Avocado", "Cheese Cubes", "Deviled Eggs"],
            "Paleo": ["Mixed Nuts", "Fruit Salad", "Vegetable Sticks"]
        }

        drink_options = ["Water", "Soda", "Lemonade", "Green Tea", "Coffee", "Smoothie"]

        def randomize_meal():
            diet = diet_var.get()
            if diet in food_options:
                meal = random.choice(food_options[diet])
                side = random.choice(side_options[diet])
                drink = random.choice(drink_options)
                suggestion = f"Meal: {meal}\nSide: {side}\nDrink: {drink}"
                CTkMessagebox(title="Randomized Meal Suggestion", message=suggestion)
            else:
                CTkMessagebox(title="Error", message="Please select a valid diet", icon='warning')

        # Function to finalize the user's selected meal
        def finalize_meal():
            selected_meal = meal_var.get()
            selected_side = side_var.get()
            selected_drink = drink_var.get()
            selected_day = day_var.get()  # Get the selected day
            if selected_meal and selected_side and selected_drink:
                # Save the selection to the corresponding day
                meal_schedule[selected_day] = dict(meal=selected_meal, side=selected_side, drink=selected_drink)
                # Update the label for the selected day
                day_labels[selected_day].configure(
                    text=f"{selected_day}: {selected_meal}, {selected_side}, {selected_drink}")
                CTkMessagebox(title="Finalized Meal",
                              message=f"Meal saved for {selected_day}:\nMeal: {selected_meal}\nSide: {selected_side}\n"
                                      f"Drink: {selected_drink}")
            else:
                CTkMessagebox(title="Error", message="Please select a meal, side, and drink", icon='warning')

        # Function to display foods that match the selected diet
        def display_matching_foods():
            diet = diet_var.get()
            if diet in food_options:
                meal_menu.configure(values=food_options[diet])
                side_menu.configure(values=side_options[diet])

        # Dropdown for selecting the day of the week
        ctk.CTkLabel(self, text="Select Day of the Week:").place(anchor='nw', y=50, x=25)
        day_var = ctk.StringVar(value="Monday")
        day_menu = ctk.CTkComboBox(self, variable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday",
                                                                   "Friday", "Saturday", "Sunday"])
        day_menu.place(anchor='nw', y=80, x=25)

        # Dropdown for selecting diet type
        ctk.CTkLabel(self, text="Select Your Diet:").place(anchor='nw', y=120, x=25)
        diet_var = ctk.StringVar(value="None")
        diet_menu = ctk.CTkComboBox(self, variable=diet_var, values=["None", "Vegetarian", "Vegan", "Keto", "Paleo"],
                                    command=lambda event: display_matching_foods())
        diet_menu.place(anchor='nw', y=150, x=25)

        # Meal selection
        ctk.CTkLabel(self, text="Select Meal:").place(anchor='nw', y=190, x=25)
        meal_var = ctk.StringVar()
        meal_menu = ctk.CTkComboBox(self, variable=meal_var, values=[])
        meal_menu.place(anchor='nw', y=220, x=25)

        # Side selection
        ctk.CTkLabel(self, text="Select Side:").place(anchor='nw', y=260, x=25)
        side_var = ctk.StringVar()
        side_menu = ctk.CTkComboBox(self, variable=side_var, values=[])
        side_menu.place(anchor='nw', y=290, x=25)

        # Drink selection
        ctk.CTkLabel(self, text="Select Drink:").place(anchor='nw', y=330, x=25)
        drink_var = ctk.StringVar(value="Water")
        drink_menu = ctk.CTkComboBox(self, variable=drink_var, values=drink_options)
        drink_menu.place(anchor='nw', y=360, x=25)

        # Finalize Meal Button
        ctk.CTkButton(self, text="Finalize Meal", font=('Helvetica', 15, 'bold'),
                      fg_color="#FF8433", hover_color="#FF6500",
                      command=finalize_meal).place(anchor='nw', y=420, x=25)

        # Button to randomize a meal suggestion
        ctk.CTkButton(self, text="Randomize Meal", font=('Helvetica', 15, 'bold'),
                      fg_color="#FF8433", hover_color="#FF6500",
                      command=randomize_meal).place(anchor='nw', y=460, x=25)

        # List to store meal selections for each day
        meal_schedule = {day: None for day in ["Monday", "Tuesday", "Wednesday", "Thursday",
                                               "Friday", "Saturday", "Sunday"]}

        # Create a dictionary to hold labels for each day
        day_labels = {}

        # Create a frame for the days of the week
        days_frame = ctk.CTkFrame(self)
        days_frame.place(x=200, y=50, anchor='nw')  # Adjust 'rely' to position higher

        # Label for days of the week
        ctk.CTkLabel(days_frame, text="Days of the Week:").pack(pady=5)

        # Display the days of the week and create labels for each day
        for day in meal_schedule.keys():
            day_label = ctk.CTkLabel(days_frame, text=f"{day}: -not set-")
            day_label.pack(anchor="w")
            day_labels[day] = day_label  # Store the label in the dictionary


class CalcPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        button = ctk.CTkButton(self, text="Calculate", command=lambda: controller.show_frames(SummaryPage))
        button.place(anchor='nw', y=100, x=250)


if __name__ == '__main__':
    run = Main()
    run.mainloop()
