import sys
import tkinter as tk
from tkinter import scrolledtext

EXIT_KEYWORDS = ["exit", "quit", "bye"]


def get_response(user_in):
    return f"You said '{user_in}'"


def show_response(event=None):
    # Function to display the CopyCat response in the GUI

    user_in = input_box.get("1.0", tk.END).strip()
    input_box.delete("1.0", tk.END)
    log.config(state=tk.NORMAL)

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


# Main GUI window
window = tk.Tk()
window.title("Stop copying me")

# Chat log
log = scrolledtext.ScrolledText(window, width=60, height=20, wrap=tk.WORD)
log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

exit_words = EXIT_KEYWORDS
welcome_message = f'Welcome! My name is CopyCat. \
Enter any of the following to quit: {exit_words}.\n'

log.insert(tk.END, welcome_message)
log.config(state=tk.DISABLED)

# User input box
input_box = scrolledtext.ScrolledText(
    window, width=40, height=4, wrap=tk.WORD)
input_box.grid(row=1, column=0, padx=10, pady=10)

# Send button
send = tk.Button(window, text="Send", command=show_response)
send.grid(row=1, column=1, padx=10, pady=10)
input_box.bind("<Return>", show_response)

# Start the GUI event loop
window.mainloop()
