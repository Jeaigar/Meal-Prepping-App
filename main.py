from tkinter import messagebox
from subprocess import call
from CTkMessagebox import CTkMessagebox, ctkmessagebox
import customtkinter as ctk
import random
from customtkinter import CTkButton

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
    if selected_meal and selected_side and selected_drink:
        CTkMessagebox(title="Finalized Meal", message=f"Meal: {selected_meal}\nSide: {selected_side}\nDrink: {selected_drink}")
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
root.geometry("400x600")  # Adjusted window size
root.iconbitmap(r"appicon.ico")
root.resizable(False, False)
root.eval("tk::PlaceWindow . center")

# Enable DPI scaling
enable_high_dpi_awareness()

# Set dark mode
# set_dark_mode()
ctk.set_appearance_mode("dark")

# BUTTON THAT ALLOWS USER TO SIGN OUT OF THEIR ACCOUNT
sign_out = CTkButton(root, text="Sign Out", command=logout, height=30, width=20, fg_color='dark red')
sign_out.place(anchor='nw')

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



# Start the Tkinter loop
root.mainloop()
