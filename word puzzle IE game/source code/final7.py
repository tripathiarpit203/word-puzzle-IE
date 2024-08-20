import tkinter as tk

# Function to check if the selected word is correct
def check_word(selected_buttons, correct_words, word_buttons, scientist_info, info_panel):
    selected_word = ''.join([btn['text'] for btn in selected_buttons]).lower()
    correct_words_lower = [word.lower() for word in correct_words]

    if selected_word in correct_words_lower:
        for btn in selected_buttons:
            btn.config(bg="cyan", state="disabled")  # Correct word: change color to cyan and disable the buttons
        correct_word_index = correct_words_lower.index(selected_word)
        update_word_list(correct_words[correct_word_index], word_buttons)
        show_scientist_info(correct_words[correct_word_index], scientist_info, info_panel)
        correct_words.pop(correct_word_index)
    else:
        reset_selection(selected_buttons)

# Function to reset selection (for incorrect words)
def reset_selection(selected_buttons):
    for btn in selected_buttons:
        if btn['state'] != 'disabled':  # Only reset buttons that are not disabled
            btn.config(bg="SystemButtonFace")

# Function to handle button press
def handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, scientist_info, info_panel):
    if event.type == tk.EventType.ButtonPress:
        reset_selection(selected_buttons)
        selected_buttons.clear()
        select_button(event.widget, selected_buttons)
    elif event.type == tk.EventType.Motion:
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if isinstance(widget, tk.Button) and widget not in selected_buttons:
            select_button(widget, selected_buttons)
    elif event.type == tk.EventType.ButtonRelease:
        check_word(selected_buttons, correct_words, word_buttons, scientist_info, info_panel)

# Function to handle button selection
def select_button(button, selected_buttons):
    selected_buttons.append(button)
    button.config(bg="yellow")

# Function to update the word list (crossing out the correct word)
def update_word_list(found_word, word_buttons):
    for btn in word_buttons:
        if btn['text'].lower() == found_word.lower():
            btn.config(fg="gray", bg="lightgray", state="disabled")  # Discolor and disable the correct word button
            break

# Function to show scientist info in the info panel
def show_scientist_info(scientist_key, scientist_info, info_panel):
    name, image, description = scientist_info[scientist_key]
    for widget in info_panel.winfo_children():
        widget.destroy()
    tk.Label(info_panel, text=name, font="Arial 14 bold").pack(pady=10)
    tk.Label(info_panel, image=image).pack()
    tk.Label(info_panel, text=description, wraplength=200, justify="left").pack(pady=10)

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

# Configure grid to resize dynamically
for i in range(len(crossword)):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Create the main frame that will hold the grid, word list, and info panel
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for the word list on the leftmost side (20% of width)
word_list_frame = tk.Frame(main_frame, width=200)
word_list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Create the grid of buttons (60% of width)
grid_frame = tk.Frame(main_frame)
grid_frame.grid(row=0, column=1, sticky="nsew")

# Create a frame for the scientist info (20% of width)
info_panel = tk.Frame(main_frame, width=200)
info_panel.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

# Create the list of words as buttons in the word list frame
word_buttons = []
for word in correct_words:
    btn = tk.Button(word_list_frame, text=word, font="Arial 10 bold", anchor="w", width=20, height=2)
    btn.pack(fill=tk.X, pady=5)
    word_buttons.append(btn)

# Create the grid of buttons inside larger frames with added spacing
button_grid = []
selected_buttons = []

for i in range(len(crossword)):
    row = []
    for j in range(len(crossword[i])):
        frame = tk.Frame(grid_frame, width=60, height=60, padx=5, pady=5)  # Added padding for spacing
        frame.grid_propagate(False)  # Prevent frame from resizing
        frame.grid(row=i, column=j, sticky="nsew")

        letter = crossword[i][j]
        btn = tk.Button(frame, text=letter, width=2, height=1)  # Smaller button, centered
        btn.pack(expand=True)  # Center the button in the frame
        btn.bind("<ButtonPress-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, scientist_info, info_panel))
        btn.bind("<B1-Motion>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, scientist_info, info_panel))
        btn.bind("<ButtonRelease-1>", lambda event: handle_button_event(event, selected_buttons, button_grid, correct_words, word_buttons, scientist_info, info_panel))
        row.append(btn)
    button_grid.append(row)

# Temporary placeholder for scientist info (this will be replaced by actual images and data)
scientist_info = {
    "HenryFord": ("Henry Gantt", tk.PhotoImage(file="C:/Users/ta203/OneDrive/Documents/ie  assn1/word puzzle IE game/assets/cards/cards/henryford.png"), "Economist and philosopher"),
}

# Run the main loop
root.mainloop()
