import sqlite3
from tkinter import messagebox
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

# Enable DPI scaling
enable_high_dpi_awareness()

# Set dark mode
# set_dark_mode()
ctk.set_appearance_mode("dark")


account_icon = ctk.CTkImage(Image.open("account_icon.png"))
account_icon._size = 150, 100
account_icon_label = ctk.CTkLabel(root, image=account_icon, text='')
account_icon_label.place(anchor='nw', y=20)

# BUTTON THAT ALLOWS USER TO SIGN OUT OF THEIR ACCOUNT
sign_out = CTkButton(root, text="Sign Out", command=logout, height=30, width=20, fg_color='dark red')
sign_out.place(anchor='nw', y=140, x=45)


# Dropdown for selecting the day of the week
ctk.CTkLabel(root, text="Select Day of the Week:").pack(pady=5)
day_var = ctk.StringVar(value="Monday")
day_menu = ctk.CTkComboBox(root, variable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
day_menu.pack()

# Dropdown for selecting diet type
ctk.CTkLabel(root, text="Select Your Diet:").pack(pady=5)
diet_var = ctk.StringVar(value="None")
diet_menu = ctk.CTkComboBox(root, variable=diet_var, values=["None", "Vegetarian", "Vegan", "Keto", "Paleo"], command= lambda event: display_matching_foods())
diet_menu.pack()

# Meal selection
ctk.CTkLabel(root, text="Select Meal:").pack(pady=5)
meal_var = ctk.StringVar()
meal_menu = ctk.CTkComboBox(root, variable=meal_var, values=[])
meal_menu.pack()

# Side selection
ctk.CTkLabel(root, text="Select Side:").pack(pady=5)
side_var = ctk.StringVar()
side_menu = ctk.CTkComboBox(root, variable=side_var, values=[])
side_menu.pack()

# Drink selection
ctk.CTkLabel(root, text="Select Drink:").pack(pady=5)
drink_var = ctk.StringVar(value="Water")
drink_menu = ctk.CTkComboBox(root, variable=drink_var, values=drink_options)
drink_menu.pack()

# Finalize Meal Button
ctk.CTkButton(root, text="Finalize Meal", command=finalize_meal).pack(pady=10)

# Button to randomize a meal suggestion
ctk.CTkButton(root, text="Randomize Meal", command=randomize_meal).pack(pady=5)

# Label to display foods and sides matching the selected diet
ctk.CTkLabel(root, text="Foods and Sides that match your diet:").pack(pady=5, anchor="w")
food_list_label = ctk.CTkLabel(root, text="", anchor="w", justify="left")
food_list_label.pack(fill="both", expand=True, padx=10, side="left")

## -- UNABLE TO USE WITH CUSTOMTKINTER -- USED THE COMMAND OPTION OF CTKCOMBOBOX INSTEAD ##
# Update food list when diet is selected
# diet_menu.bind("<<ComboboxSelected>>", lambda event: display_matching_foods())

# List to store meal selections for each day
meal_schedule = {day: None for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

# Create a dictionary to hold labels for each day
day_labels = {}

# Create a frame for the days of the week
days_frame = ctk.CTkFrame(root)
days_frame.place(relx=0.65, rely=0.1, anchor='nw')  # Adjust 'rely' to position higher

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
