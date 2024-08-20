import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Interactive Criss-Cross Puzzle")
root.configure(bg="#f0f0f0")

# Define correct words and scientist details (update with actual paths to images and details)
correct_words = [
    "AdamSmith", "CharlesBabbage", "EdwardsDeming",
    "EliWhitney", "EltonMayo", "FrederickWTaylor",
    "HenryFord", "HenryGantt",
    "JamesPWomack", "JohnPKotter", "JoshepMJuran",
    "KaoruIshikawa", "KurtLewin", "MorrisCooke",
    "PeterSenge", "ShigeoShingo", "TaiichiOhno",
    "WalterAShewhart"
]

# Create PhotoImage objects after root window is initialized
scientist_details = {
    "AdamSmith": ("Adam Smith", tk.PhotoImage(file="adam_smith.png"), "Economist and philosopher"),
    "CharlesBabbage": ("Charles Babbage", tk.PhotoImage(file="charles_babbage.png"), "Father of the computer"),
    # Add more scientists' details here
}

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_labels, scientist_details):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="cyan", state="disabled")  # Correct word: change color to cyan and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_labels)
        show_scientist_details(correct_words[correct_word_index], scientist_details)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="white")

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, scientist_details):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_labels, scientist_details)

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="yellow")

# Function to update the word list (crossing out the correct word)
def update_word_list(found_word, word_labels):
    for lbl in word_labels:
        if lbl['text'].lower() == found_word.lower():
            lbl.config(fg="gray", font="Arial 10 overstrike")
            break

# Function to show scientist details
def show_scientist_details(scientist, scientist_details):
    if scientist in scientist_details:
        name, image, details = scientist_details[scientist]
        details_label.config(text=f"{name}\n\n{details}")
        photo_label.config(image=image)
        photo_label.image = image  # Keep a reference to prevent garbage collection

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

# Create the main frame
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Configure grid to resize dynamically
for i in range(len(crossword)):
    main_frame.grid_rowconfigure(i, weight=1)
    main_frame.grid_columnconfigure(i, weight=1)

# Create the grid of buttons inside larger frames
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        frame = tk.Frame(main_frame, width=60, height=60, bg="#e6e6e6", bd=2, relief="raised")  # Larger frame for spacing
        frame.grid_propagate(False)  # Prevent frame from resizing
        frame.grid(row=i, column=j, sticky="nsew")

        letter = crossword[i][j]
        btn = tk.Button(frame, text=letter, width=2, height=1, bg="white", font="Arial 12 bold", relief="flat")
        btn.pack(expand=True)  # Center the button in the frame
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, scientist_details))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, scientist_details))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_labels, scientist_details))
        row.append(btn)
    button_grid.append(row)

# Create a list of words outside the grid
word_labels = []
for idx, word in enumerate(correct_words):
    lbl = tk.Label(main_frame, text=word, font="Arial 10 bold", bg="#f0f0f0")
    lbl.grid(row=idx, column=len(crossword[0]) + 1, padx=10, sticky="w")
    word_labels.append(lbl)

# Create a sidebar for scientist details
sidebar = tk.Frame(root, width=200, bg="#f0f0f0", bd=2, relief="ridge")
sidebar.pack(side="right", fill="y", padx=10)

photo_label = tk.Label(sidebar, bg="#f0f0f0")
photo_label.pack(pady=10)

details_label = tk.Label(sidebar, bg="#f0f0f0", font="Arial 10", justify="left", wraplength=180)
details_label.pack(pady=10)

# Run the main loop
root.mainloop()
