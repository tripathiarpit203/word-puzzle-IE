import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_labels, name_label, image_label):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="pink", state="disabled")  # Correct word: change color to pink and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_labels, name_label, image_label)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="lightblue")

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, name_label, image_label):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_labels, name_label, image_label)

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="lavender")

# Function to update the word list (crossing out the correct word) and display the image
def update_word_list(found_word, word_labels, name_label, image_label):
    for lbl in word_labels:
        if lbl['text'].lower() == found_word.lower():
            lbl.config(fg="gray", font="Arial 10 overstrike")
            break
    show_image(found_word, name_label, image_label)

# Function to set the image paths
def get_image_path(word):
    images = {
        "AdamSmith": "images/adam_smith.jpg",
        "CharlesBabbage": "images/charles_babbage.jpg",
        "EdwardsDeming": "images/edwards_deming.jpg",
        "EliWhitney": "images/eli_whitney.jpg",
        "EltonMayo": "images/elton_mayo.jpg",
        "FrederickWTaylor": "images/frederick_taylor.jpg",
        "HenryFord": "C:/Users/ta203/OneDrive/Documents/ie  assn1/word puzzle IE game/assets/cards/cards/henryford.png",
        "HenryGantt": "images/henry_gantt.jpg",
        "JamesPWomack": "images/james_womack.jpg",
        "JohnPKotter": "images/john_kotter.jpg",
        "JoshepMJuran": "images/joshep_juran.jpg",
        "KaoruIshikawa": "images/kaoru_ishikawa.jpg",
        "KurtLewin": "images/kurt_lewin.jpg",
        "MorrisCooke": "images/morris_cooke.jpg",
        "PeterSenge": "images/peter_senge.jpg",
        "ShigeoShingo": "images/shigeo_shingo.jpg",
        "TaiichiOhno": "images/taiichi_ohno.jpg",
        "WalterAShewhart": "images/walter_shewhart.jpg"
    }
    return images.get(word, None)

# Check for the correct resampling method
try:
    resampling_method = Image.Resampling.LANCZOS
except AttributeError:
    # Fallback for older Pillow versions
    resampling_method = Image.LANCZOS

# Function to display the image and name
def show_image(word, name_label, image_label):
    image_path = get_image_path(word)
    name_label.config(text=word)
    
    if image_path:
        image = Image.open(image_path)
        image = image.resize((300,475), resampling_method)  # Use the correct resampling method
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to avoid garbage collection

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

# Create a frame for the word list (left sidebar)
sidebar_frame = tk.Frame(root, bg="lavender", relief="solid", bd=1)
sidebar_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

# Create Canvas for background
canvas = Canvas(root)
canvas.grid(row=0, column=1,padx=10, pady=10, sticky="nsew")
canvas.create_image(0, 0, anchor="nw")

# Create a frame for the grid
grid_frame = tk.Frame(canvas, bg="lavender", relief="solid", bd=1)
canvas.create_window((0, 0), window=grid_frame, anchor="nw")

# Create a frame for the image section
image_section_frame = tk.Frame(root, bg="lavender", relief="solid", bd=1)
image_section_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Add a label for the selected name
name_label = tk.Label(image_section_frame, text="", font=("Arial", 20, "bold"), bg="lavender", fg="black")
name_label.pack(pady=10)

# Label to display the image
image_label = tk.Label(image_section_frame, bg="lavender")
image_label.pack(expand=True)  # Make it fill the remaining space

# Configure grid to resize dynamically
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Adjust this scale to control button size changes
button_size = 40

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
        btn.grid(row=i, column=j, padx=6, pady=6, ipadx=1.3, ipady=1.3, sticky="nsew")
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, name_label, image_label))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, name_label, image_label))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, name_label, image_label))
        row.append(btn)
    button_grid.append(row)

# Create the list of words as labels in the sidebar
word_buttons = []
for word in correct_words:
    btn = tk.Button(sidebar_frame, text=word, font="Arial 10 bold", bg="lightblue", relief="flat")
    btn.pack(fill=tk.X, pady=6.5, padx=10)
    word_buttons.append(btn)

# Function to resize the grid when the window size changes
def resize_grid(event):
    global button_size
    grid_width = min(event.width, event.height)
    button_size = grid_width // len(crossword)

    for i in range(len(button_grid)):
        for j in range(len(button_grid[i])):
            btn = button_grid[i][j]
            btn.config(width=button_size//14, height=button_size//23, font=("Arial", button_size//4))

# Bind the resize function to the canvas resize event
canvas.bind("<Configure>", resize_grid)

# Run the main loop
root.mainloop()
