import tkinter as tk
from tkinter import ttk, messagebox
import random

# Food, sides, and drinks corresponding to each diet
food_options = {
    "None": ["Pizza", "Burger", "Fries"],
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
        messagebox.showinfo("Meal Suggestion", suggestion)
    else:
        messagebox.showwarning("Error", "Please select a valid diet")

# Function to display foods that match the selected diet
def display_matching_foods():
    diet = diet_var.get()
    if diet in food_options:
        matching_foods = "\n".join(food_options[diet])
        matching_sides = "\n".join(side_options[diet])
        food_list_label.config(text=f"Foods:\n{matching_foods}\n\nSides:\n{matching_sides}")
    else:
        food_list_label.config(text="No foods available for this diet.")

# Enable dark mode theme
def set_dark_mode():
    root.tk_setPalette(background="#2E2E2E", foreground="#FFFFFF", activeBackground="#505050", activeForeground="#FFFFFF")
    root.configure(bg="#2E2E2E")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#2E2E2E", foreground="white")
    style.configure("TButton", background="#505050", foreground="white")
    style.configure("TCombobox", fieldbackground="#505050", background="#505050", foreground="white")

# Create the main window
root = tk.Tk()
root.title("Meal Prepping App")
root.geometry("400x300")

# Set dark mode
set_dark_mode()

# Dropdown for selecting the day of the week
ttk.Label(root, text="Select Day of the Week:").pack(pady=5)
day_var = tk.StringVar(value="Monday")
day_menu = ttk.Combobox(root, textvariable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
day_menu.pack()

# Dropdown for selecting diet type
ttk.Label(root, text="Select Your Diet:").pack(pady=5)
diet_var = tk.StringVar(value="None")
diet_menu = ttk.Combobox(root, textvariable=diet_var, values=["None", "Vegetarian", "Vegan", "Keto", "Paleo"])
diet_menu.pack()

# Button to randomize a meal suggestion
ttk.Button(root, text="Randomize Meal", command=randomize_meal).pack(pady=10)

# Label to display foods and sides matching the selected diet
ttk.Label(root, text="Foods and Sides that match your diet:").pack(pady=5, anchor="w")
food_list_label = ttk.Label(root, text="", anchor="w", justify="left")
food_list_label.pack(fill="both", expand=True, padx=10, side="left")

# Update food list when diet is selected
diet_menu.bind("<<ComboboxSelected>>", lambda event: display_matching_foods())

# Start the Tkinter loop
root.mainloop()
