import tkinter as tk
from tkinter import messagebox, scrolledtext
import winsound  # Built-in Windows module for playing beeps
import time

# -------------------------
# Morse Code Dictionaries
# -------------------------
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.',
    ' ': '/',  # Space between words
    '.': '.-.-.-', ',': '--..--', '?': '..--..',
    '!': '-.-.--', ':': '---...', "'": '.----.',
    '-': '-....-', '/': '-..-.', '(': '-.--.',
    ')': '-.--.-', '&': '.-...', ';': '-.-.-.'
}

# Reverse dictionary for decoding Morse code
MORSE_CODE_DICT_REVERSE = {v: k for k, v in MORSE_CODE_DICT.items()}

# -------------------------
# Theme settings
# -------------------------
LIGHT_BG, LIGHT_FG = "#f0f0f0", "#000000"
DARK_BG, DARK_FG = "#1e1e1e", "#ffffff"
current_theme = "light"


# -------------------------
# Conversion Functions
# -------------------------
def text_to_morse(text):
    """Convert text to Morse code."""
    morse_text = ''
    unsupported = False
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_text += MORSE_CODE_DICT[char] + ' '
        else:
            unsupported = True
    if unsupported:
        messagebox.showinfo("Notice", "Some characters were ignored (unsupported).")
    return morse_text.strip()


def morse_to_text(morse):
    """Convert Morse code to text."""
    decoded_text = ''
    words = morse.split(' / ')  # Words separated by '/'
    unsupported = False
    for word in words:
        letters = word.split()  # Letters separated by spaces
        for letter in letters:
            if letter in MORSE_CODE_DICT_REVERSE:
                decoded_text += MORSE_CODE_DICT_REVERSE[letter]
            else:
                unsupported = True
        decoded_text += ' '
    if unsupported:
        messagebox.showinfo("Notice", "Some Morse sequences were ignored (unsupported).")
    return decoded_text.strip()


# -------------------------
# Sound playback using winsound
# -------------------------
def play_morse_sound(morse_code):
    """
    Play Morse code using system beeps:
    '.' = short beep, '-' = long beep, ' ' = letter space, '/' = word space
    """
    for symbol in morse_code:
        if symbol == '.':
            winsound.Beep(800, 100)  # short beep (dot)
        elif symbol == '-':
            winsound.Beep(800, 300)  # long beep (dash)
        elif symbol == ' ':
            time.sleep(0.1)  # short pause between letters
        elif symbol == '/':
            time.sleep(0.3)  # pause between words


# -------------------------
# GUI Button Functions
# -------------------------
def convert_to_morse():
    text = text_entry.get()
    if text:
        morse = text_to_morse(text)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, morse)
        play_morse_sound(morse)  # Play Morse code sound
    else:
        messagebox.showwarning("Input Error", "Please enter text to convert!")


def convert_to_text():
    morse = text_entry.get()
    if morse:
        decoded = morse_to_text(morse)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, decoded)
    else:
        messagebox.showwarning("Input Error", "Please enter Morse code to convert!")


def clear_all():
    """Clear input and output fields."""
    text_entry.delete(0, tk.END)
    output_text.delete(1.0, tk.END)


def copy_output():
    """Copy output text to clipboard."""
    result = output_text.get(1.0, tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        messagebox.showinfo("Copied", "Output copied to clipboard!")


def toggle_theme():
    """Toggle between light and dark themes."""
    global current_theme
    if current_theme == "light":
        root.configure(bg=DARK_BG)
        text_entry.configure(bg=DARK_BG, fg=DARK_FG, insertbackground=DARK_FG)
        output_text.configure(bg=DARK_BG, fg=DARK_FG)
        for widget in btn_frame.winfo_children():
            widget.configure(bg=DARK_BG, fg=DARK_FG)
        current_theme = "dark"
    else:
        root.configure(bg=LIGHT_BG)
        text_entry.configure(bg=LIGHT_BG, fg=LIGHT_FG, insertbackground=LIGHT_FG)
        output_text.configure(bg=LIGHT_BG, fg=LIGHT_FG)
        for widget in btn_frame.winfo_children():
            widget.configure(bg=LIGHT_BG, fg=LIGHT_FG)
        current_theme = "light"


# -------------------------
# GUI Setup
# -------------------------
root = tk.Tk()
root.title("Text ↔ Morse Code Converter")
root.geometry("700x500")
root.resizable(False, False)
root.configure(bg=LIGHT_BG)

# Fonts
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 11)

# Input
tk.Label(root, text="Enter Text or Morse Code:", font=label_font, bg=LIGHT_BG).pack(pady=10)
text_entry = tk.Entry(root, width=65, font=label_font, bg=LIGHT_BG, fg=LIGHT_FG, insertbackground=LIGHT_FG)
text_entry.pack(pady=5)

# Buttons
btn_frame = tk.Frame(root, bg=LIGHT_BG)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Text → Morse", command=convert_to_morse, width=15, font=button_font).grid(row=0, column=0,
                                                                                                     padx=5)
tk.Button(btn_frame, text="Morse → Text", command=convert_to_text, width=15, font=button_font).grid(row=0, column=1,
                                                                                                    padx=5)
tk.Button(btn_frame, text="Clear", command=clear_all, width=10, font=button_font).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Copy Output", command=copy_output, width=12, font=button_font).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Toggle Theme", command=toggle_theme, width=12, font=button_font).grid(row=0, column=4,
                                                                                                 padx=5)

# Output
tk.Label(root, text="Output:", font=label_font, bg=LIGHT_BG).pack(pady=10)
output_text = scrolledtext.ScrolledText(root, height=15, width=80, font=label_font, bg=LIGHT_BG, fg=LIGHT_FG)
output_text.pack(pady=5)

# Run the GUI
root.mainloop()
