"""Sys provides functionality to exit the program. tkinter provides UI."""
import sys
import tkinter as tk
from tkinter import scrolledtext

EXIT_KEYWORDS = ["exit", "quit", "bye"]


def get_response(user_in):
    '''
    Gets the user's response and just copies it back. This is only a function
    because it may get updated to respond differently in the future. For now
    it may seem a bit redundant or useless.
    '''
    return f"You said '{user_in}'"


def show_response(event=None):  # pylint: disable=unused-argument
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

# The chat log
log = scrolledtext.ScrolledText(window, width=60, height=20, wrap=tk.WORD)
log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

exit_words = EXIT_KEYWORDS
welcome_message = f'Welcome! My name is CopyCat. \
Enter any of the following to quit: {exit_words}.\n'  # May edit later...

log.insert(tk.END, welcome_message)
log.config(state=tk.DISABLED)  # Do not want user to be able to type in log

# User input box (below the log)
input_box = scrolledtext.ScrolledText(
    window, width=40, height=4, wrap=tk.WORD)
input_box.grid(row=1, column=0, padx=10, pady=10)

# Send button (beside the user input box)
send = tk.Button(window, text="Send", command=show_response)
send.grid(row=1, column=1, padx=10, pady=10)
input_box.bind("<Return>", show_response)

# Start the UI event loop
window.mainloop()
