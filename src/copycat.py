"""Sys provides functionality to exit the program. tkinter provides UI.
Regex for punctuation matching"""
import sys
import re
import tkinter as tk
from tkinter import scrolledtext

EXIT_KEYWORDS = ["exit", "quit", "bye"]


def arr_to_string(arr: list) -> str:
    '''
    Clean array to string
    '''
    res = ""
    for word in arr:
        res += word + ", "
    return res[:-2]


def get_response(user_in: str) -> str:
    '''
    Gets the user's response and just copies it back. This is only a function
    because it may get updated to respond differently in the future. For now
    it may seem a bit redundant or useless.
    '''

    if re.match(r'[^\w\s]', user_in[-1]):
        # Don't want extra punctuation
        user_in = re.sub(r'[^\w\s]', '', user_in[:-1])
    return f'{user_in.strip()}!'


def show_response(event=None) -> None:  # pylint: disable=unused-argument
    '''
    Displays the CopyCat response in the GUI alongside the user input
    '''

    user_in = input_area.get("1.0", tk.END).strip()
    input_area.delete("1.0", tk.END)
    # DISABLED -> NORMAL to allow tk to show stuff
    chat_log.config(state=tk.NORMAL)

    if user_in.lower() in EXIT_KEYWORDS:
        chat_log.insert(tk.END, "CopyCat: Goodbye!\n")
        chat_log.see(tk.END)
        sys.exit(0)

    chat_log.insert(tk.END, "You: " + user_in + "\n")
    chat_log.see(tk.END)
    response = get_response(user_in)
    chat_log.insert(tk.END, "CopyCat: " + response + "\n")
    chat_log.see(tk.END)
    chat_log.config(state=tk.DISABLED)

    return 'break'  # Stops \n from staying in the user input area


# Main window
window = tk.Tk()
window.title("Stop copying me")


def create_chat_log():
    """
    Creates the chat log
    """
    log = scrolledtext.ScrolledText(window, width=60, height=20, wrap=tk.WORD,
                                    bd=30, relief=tk.FLAT,
                                    highlightbackground="white",
                                    highlightthickness=3)
    log.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    return log


# The chat log
chat_log = create_chat_log()


def get_exit_words() -> list:
    """EXIT_KEYWORDS getter"""
    return EXIT_KEYWORDS


def create_welcome_message():
    """
    Welcome message for the chat log
    """
    exit_words = get_exit_words()
    msg = 'Welcome! My name is CopyCat. '
    msg += f'Enter any of the following to quit: {arr_to_string(exit_words)}.'
    msg += '\n\n'
    # May edit later...

    chat_log.insert(tk.END, msg)
    # Do not want user to be able to type in log
    chat_log.config(state=tk.DISABLED)


create_welcome_message()
PLACEHOLDER_TEXT = "Type your message here..."


def add_placeholder(event=None):
    """
    Adds placeholder text if the input box is empty
    """
    if not input_area.get("1.0", tk.END).strip():
        input_area.insert("1.0", PLACEHOLDER_TEXT)


def remove_placeholder(event=None):
    """
    Removes placeholder text when the user starts typing
    """
    if input_area.get("1.0", tk.END).strip() == PLACEHOLDER_TEXT:
        input_area.delete("1.0", tk.END)


def create_user_input_area():
    """
    Creates the user input area
    """
    # User input box (below the log)
    input_box = tk.Text(window, width=40, height=4, wrap=tk.WORD,
                        relief=tk.FLAT, bd=5, highlightbackground="white",
                        highlightthickness=2)
    input_box.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    # User input scrollbar (hidden initially)
    user_input_scrollbar = tk.Scrollbar(window, command=input_box.yview)
    input_box.config(yscrollcommand=user_input_scrollbar.set)

    # Add placeholder text
    input_box.insert("1.0", PLACEHOLDER_TEXT)
    input_box.bind("<FocusIn>", remove_placeholder)
    input_box.bind("<FocusOut>", add_placeholder)
    # input_box.config(fg="white")  # Not needed but here if I choose to use

    # Send button (beside the user input box)
    send = tk.Button(window, text="Send", command=show_response)
    send.grid(row=1, column=1, padx=10, pady=10, sticky='e')
    return input_box


input_area = create_user_input_area()
input_area.bind("<Return>", show_response)  # Enter/Return to send

# Start the UI event loop
window.minsize(375, 400)
# Makes the window resizable
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.mainloop()
