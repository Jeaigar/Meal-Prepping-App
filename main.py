import sqlite3
from tkinter import messagebox
from tkinter import ttk
from subprocess import call
from CTkMessagebox import CTkMessagebox, ctkmessagebox
import customtkinter as ctk
import random
from customtkinter import CTkButton
from PIL import Image, ImageTk


# Food, sides, and drinks corresponding to each diet
food_options = {
    "None": ["Pizza", "Burger", "Burrito"],
    "Vegetarian": ["Grilled Vegetables", "Vegetable Stir Fry", "Lentil Soup"],
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


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Function to randomize a meal suggestion based on the selected diet
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
        meal_schedule[selected_day] = {
            "meal": selected_meal,
            "side": selected_side,
            "drink": selected_drink
        }
        # Update the label for the selected day
        day_labels[selected_day].configure(text=f"{selected_day}: {selected_meal}, {selected_side}, {selected_drink}")
        CTkMessagebox(title="Finalized Meal", message=f"Meal saved for {selected_day}:\nMeal: {selected_meal}\nSide: {selected_side}\nDrink: {selected_drink}")
    else:
        CTkMessagebox(title="Error", message="Please select a meal, side, and drink", icon='warning')


# Function to display foods that match the selected diet
def display_matching_foods():
    diet = diet_var.get()
    if diet in food_options:
        matching_foods = "\n".join(food_options[diet])
        matching_sides = "\n".join(side_options[diet])
        food_list_label.configure(text=f"Foods:\n{matching_foods}\n\nSides:\n{matching_sides}")
        meal_menu.configure(values=food_options[diet])
        side_menu.configure(values=side_options[diet])
    else:
        food_list_label.config(text="No foods available for this diet.")


# Enable DPI awareness for better resolution on high-DPI displays
def enable_high_dpi_awareness():
    try:
        root.tk.call('tk', 'scaling', 2.0)  # Scale to make the UI sharper on high-resolution screens
    except:
        pass


def logout():
    messagebox.showinfo("Logout", "Logging out...")

    root.destroy()

    call(["python", "login.py"])


# Create the main window
root = ctk.CTk()
root.title("MealCraft")
root.geometry("1000x600")  # Adjusted window size
root.iconbitmap(r"appicon.ico")
root.resizable(False, False)
root.eval("tk::PlaceWindow . center")

# CREATES AND PLACES FRAME FOR LEFT SIDE TOOLBAR
toolbar = ctk.CTkFrame(root, height=500, width=200)
toolbar.place(x=25, y=25)

# CREATES AND PLACES FRAME FOR WIDGETS ON THE RIGHT SIDE
main_frame = ctk.CTkFrame(root, height=550, width=710)
main_frame.pack_propagate(False)
main_frame.place(x=270, y=15)

# Enable DPI scaling
enable_high_dpi_awareness()

# Set dark mode
# set_dark_mode()
ctk.set_appearance_mode("dark")


account_icon = ctk.CTkImage(Image.open("account_icon.png"))
account_icon._size = 150, 100
account_icon_label = ctk.CTkLabel(toolbar, image=account_icon, text='')
account_icon_label.place(anchor='nw', y=20, x=25)

# BUTTON THAT ALLOWS USER TO SIGN OUT OF THEIR ACCOUNT
sign_out = CTkButton(toolbar, text="Sign Out", command=logout, height=30, width=20, fg_color='dark red', font=("Arial", 12, 'bold'))
sign_out.place(anchor='nw', y=140, x=70)

# SHOWS AN OVERVIEW OF THE USERS MEALS
summary_button = ctk.CTkButton(toolbar, text="Summary", font=('Helvetica', 15, 'bold'))
summary_button.place(anchor='nw', y=200, x=25)


# TAKES USERS TO MEAL PLAN PAGE
plan_meal_button = ctk.CTkButton(toolbar, text="Plan Your Meal", font=('Helvetica', 15, 'bold'))
plan_meal_button.place(anchor='nw', y=250, x=25)

# OPENS PROMPT FOR USERS TO ASK AI FOR MEAL SUGGESTIONS
ask_button = ctk.CTkButton(toolbar, text="Not sure? Ask AI", font=('Helvetica', 15, 'bold'))
ask_button.place(anchor='nw', y=300, x=25)

# CREATES AND PLACES SEPARATOR BETWEEN TOOL BAR ON THE LEFT SIDE AND THE RIGHT SIDE
sep_frame = ctk.CTkFrame(root, height=500, width=1, bg_color='gray')
sep_frame.place(x=250,y=30)




# Dropdown for selecting the day of the week
day_label = ctk.CTkLabel(main_frame, text="Select Day of the Week:").place(anchor='nw', y=50, x=25)
day_var = ctk.StringVar(value="Monday")
day_menu = ctk.CTkComboBox(main_frame, variable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
day_menu.place(anchor='nw', y=80, x=25)

# Dropdown for selecting diet type
ctk.CTkLabel(main_frame, text="Select Your Diet:").place(anchor='nw', y=120, x=25)
diet_var = ctk.StringVar(value="None")
diet_menu = ctk.CTkComboBox(main_frame, variable=diet_var, values=["None", "Vegetarian", "Vegan", "Keto", "Paleo"], command= lambda event: display_matching_foods())
diet_menu.place(anchor='nw', y=150, x=25)

# Meal selection
ctk.CTkLabel(main_frame, text="Select Meal:").place(anchor='nw', y=190, x=25)
meal_var = ctk.StringVar()
meal_menu = ctk.CTkComboBox(main_frame, variable=meal_var, values=[])
meal_menu.place(anchor='nw', y=220, x=25)

# Side selection
ctk.CTkLabel(main_frame, text="Select Side:").place(anchor='nw', y=260, x=25)
side_var = ctk.StringVar()
side_menu = ctk.CTkComboBox(main_frame, variable=side_var, values=[])
side_menu.place(anchor='nw', y=290, x=25)

# Drink selection
ctk.CTkLabel(main_frame, text="Select Drink:").place(anchor='nw', y=330, x=25)
drink_var = ctk.StringVar(value="Water")
drink_menu = ctk.CTkComboBox(main_frame, variable=drink_var, values=drink_options)
drink_menu.place(anchor='nw', y=360, x=25)

# Finalize Meal Button
ctk.CTkButton(main_frame, text="Finalize Meal", command=finalize_meal).place(anchor='nw', y=420, x=25)

# Button to randomize a meal suggestion
ctk.CTkButton(main_frame, text="Randomize Meal", command=randomize_meal).place(anchor='nw', y=460, x=25)

# List to store meal selections for each day
meal_schedule = {day: None for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# Create a dictionary to hold labels for each day
day_labels = {}

# Create a frame for the days of the week
days_frame = ctk.CTkFrame(main_frame)
days_frame.place(x=200, y=50, anchor='nw')  # Adjust 'rely' to position higher

# Label for days of the week
ctk.CTkLabel(days_frame, text="Days of the Week:").pack(pady=5)

# Display the days of the week and create labels for each day
for day in meal_schedule.keys():
    day_label = ctk.CTkLabel(days_frame, text=f"{day}: -not set-")
    day_label.pack(anchor="w")
    day_labels[day] = day_label  # Store the label in the dictionary

# Start the Tkinter loop
if __name__ == '__main__':
    root.mainloop()
