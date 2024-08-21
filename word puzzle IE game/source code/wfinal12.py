import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageFilter

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_buttons, info_panel, scientist_images):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="pink", state="disabled")  # Correct word: change color to pink and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_buttons)
        show_scientist_info(correct_words[correct_word_index], info_panel, scientist_images)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="lightblue")

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, info_panel, scientist_images):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_buttons, info_panel, scientist_images)

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="lavender")

# Function to update the word list (crossing out the correct word)
def update_word_list(found_word, word_buttons):
    for btn in word_buttons:
        if btn['text'].lower() == found_word.lower():
            btn.config(fg="gray", state="disabled", bg="white")
            break

# Function to show scientist info on the right side
def show_scientist_info(scientist_name, info_panel, scientist_images):
    for widget in info_panel.winfo_children():
        widget.destroy()
    
    if scientist_name in scientist_images:
        image = scientist_images[scientist_name]
        image_label = tk.Label(info_panel, image=image)
        image_label.image = image  # Keep a reference to avoid garbage collection
        image_label.pack(padx=10, pady=10)

# Define the crossword puzzle as a list of lists
crossword = [
    list("EYPWEYKGXVTEJJOTOICQ"),
    list("LIKQKZWMGTLOFHSLFHIK"),
    list("ICHCMWTRNTHYLLPZACWS"),
    list("WMTZKWZAONIWELTRUKAH"),
    list("HRPXKGGNPBTHNQLEUMLC"),
    list("INOHVYMKQACAKEIXEPTO"),
    list("TQSLRAORIXRCSCJLQGEO"),
    list("NEHNYTCIVUABREVXFNRV"),
    list("EMEOTACGJMAZQENXDIAD"),
    list("YHQENHTMOBKQIKSLXMSR"),
    list("OLRYIIPWBTTNAGYRNEHO"),
    list("AUMOWEPAKKDTBOXDTDEF"),
    list("PDHOHSGSECIQEWHBTSWY"),
    list("RNASEEMORRISCOOKEDHR"),
    list("OEOMFVMOLBRRYPUMURAN"),
    list("FJAOSOGNIHSOEGIHSARE"),
    list("SJIYIMOFQHNIKDVQDWTH"),
    list("MKAORUISHIKAWAEXSDTT"),
    list("PABEZPETERSENGERSEFY"),
    list("OFQOGUNFHGIAFFMLFDGC")
]

# Define correct words
correct_words = [
    "AdamSmith", "CharlesBabbage", "EdwardsDeming",
    "EliWhitney", "EltonMayo", "FrederickWTaylor",
    "HenryFord", "HenryGantt",
    "JamesPWomack", "JohnPKotter", "JoshepMJuran",
    "KaoruIshikawa", "KurtLewin", "MorrisCooke",
    "PeterSenge", "ShigeoShingo", "TaiichiOhno",
    "WalterAShewhart"
]

# Create the main window
root = tk.Tk()
root.title("Interactive Criss-Cross Puzzle")
root.geometry("2560x1600")

# Create Canvas for background
canvas = Canvas(root)
canvas.grid(row=0, column=0, sticky="nsew")
canvas.create_image(0, 0, anchor="nw")

# Create a frame for the sidebar on the left side
sidebar_frame = tk.Frame(root, width=100, bg="white")
sidebar_frame.grid(row=0, column=0, sticky="ns")

# Create a frame for the grid in the center
grid_frame = tk.Frame(root, bg="lavender")
grid_frame.grid(row=0, column=1, sticky="nsew")

# Create a frame for the scientist info on the right side
info_panel = tk.Frame(root, width=200, bg="white")
info_panel.grid(row=0, column=2, sticky="ns")

# Configure grid to resize dynamically
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Adjust this scale to control button size changes
button_size = 10

# Create the grid of buttons inside larger frames
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        letter = crossword[i][j]

        # Create rounded rectangle buttons
        btn = tk.Button(grid_frame, text=letter, width=button_size//10, height=button_size//20, font=("Arial", 14, "bold"),
                        bg="lightblue", relief="flat", bd=0)
        btn.grid(row=i, column=j, padx=6, pady=6, ipadx=2, ipady=2, sticky="nsew")
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, info_panel, scientist_images))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, info_panel, scientist_images))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, info_panel, scientist_images))
        row.append(btn)
    button_grid.append(row)

# Create the list of words as buttons in the sidebar
word_buttons = []
for word in correct_words:
    btn = tk.Button(sidebar_frame, text=word, font="Arial 10 bold", bg="lightblue", relief="flat")
    btn.pack(fill=tk.X, pady=5, padx=10)
    word_buttons.append(btn)

# Function to resize the grid when the window size changes
def resize_grid(event):
    global button_size
    grid_width = min(event.width, event.height)
    button_size = grid_width // len(crossword)

    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            btn = button_grid[i][j]
            btn.config(width=button_size//6, height=button_size//12, font=("Arial", button_size//2))

# Bind the resize function to the canvas resize event
canvas.bind("<Configure>", resize_grid)

# Placeholder for scientist images (you'll need to provide actual paths to images)
scientist_images = {
    "HenryFord": ImageTk.PhotoImage(file="C:/Users/ta203/OneDrive/Documents/ie  assn1/word puzzle IE game/assets/cards/cards/henryford.png"),
    # Add other scientists' images here
}

# Run the main loop
root.mainloop()
