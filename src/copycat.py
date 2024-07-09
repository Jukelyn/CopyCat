"""Sys provides functionality to exit the program. tkinter provides UI."""
import sys
import tkinter as tk
from tkinter import scrolledtext

EXIT_KEYWORDS = ["exit", "quit", "bye"]


def arr_to_string(arr: list) -> str:
    '''
    Cleaner array to string
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
    return f'{user_in}!'


def show_response(event=None) -> None:  # pylint: disable=unused-argument
    '''
    Displays the CopyCat response in the GUI alongside the user input
    '''

    user_in = input_box.get("1.0", tk.END).strip()
    input_box.delete("1.0", tk.END)
    log.config(state=tk.NORMAL)  # DISABLED -> NORMAL to allow tk to show stuff

    if user_in.lower() in EXIT_KEYWORDS:
        log.insert(tk.END, "CopyCat: Goodbye!\n")
        log.see(tk.END)
        sys.exit(0)

    log.insert(tk.END, "You: " + user_in + "\n")
    log.see(tk.END)
    response = get_response(user_in)
    log.insert(tk.END, "CopyCat: " + response + "\n")
    log.see(tk.END)
    log.config(state=tk.DISABLED)


# Main window
window = tk.Tk()
window.title("Stop copying me")

# Make the window resizable
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

# The chat log
log = scrolledtext.ScrolledText(window, width=60, height=20, wrap=tk.WORD)
log.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

exit_words = EXIT_KEYWORDS
welcome_message = f'Welcome! My name is CopyCat. \
Enter any of the following to quit: {arr_to_string(exit_words)}.\n\n'  # May edit later...

log.insert(tk.END, welcome_message)
log.config(state=tk.DISABLED)  # Do not want user to be able to type in log

# User input box (below the log)
input_box = tk.Text(window, width=40, height=4, wrap=tk.WORD)
input_box.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

# User input scrollbar (hidden initially)
user_input_scrollbar = tk.Scrollbar(window, command=input_box.yview)
input_box.config(yscrollcommand=user_input_scrollbar.set)

# Send button (beside the user input box)
send = tk.Button(window, text="Send", command=show_response)
send.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

input_box.bind("<Return>", show_response)

# Start the UI event loop
window.mainloop()
