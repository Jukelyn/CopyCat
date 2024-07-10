#!/usr/bin/env python3
"""
Sys provides functionality to exit the program. tkinter provides UI.
Regex for punctuation matching
"""
import sys
import re
import tkinter as tk
from tkinter import scrolledtext

EXIT_KEYWORDS = sorted(["end", "exit", "quit", "bye"])
MSG_COUNTER = 0
SHOUTING = True


def arr_to_string(arr: list) -> str:
    """
    Clean array to string
    """
    res = ""
    for word in arr:
        res += word + ", "
    return res[:-2]


def get_response(user_in: str) -> str:
    """
    Gets the user's response and just copies it back. This is only a function
    because it may get updated to respond differently in the future. For now
    it may seem a bit redundant or useless.
    """
    global MSG_COUNTER  # pylint: disable=global-statement
    MSG_COUNTER += 1
    update_message_counter()

    if len(user_in) > 1:
        if re.match(r'[^\w\s]', user_in[-1]):
            # Don't want extra punctuation
            user_in = re.sub(r'[^\w\s]', '', user_in[:-1])

    res = f'{user_in.strip()}!' + '\n'
    return res.upper() if SHOUTING else res


def toggle_shout():
    """
    Toggles the shouting
    """
    global SHOUTING  # pylint: disable=global-statement
    SHOUTING = not SHOUTING


def show_response(event=None) -> None:  # pylint: disable=unused-argument
    """
    Displays the CopyCat response in the GUI alongside the user input
    """

    user_in = input_area.get("1.0", tk.END).strip()
    input_area.delete("1.0", tk.END)
    # DISABLED -> NORMAL to allow tk to add stuff
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
window.title("Stop copying me!")
window.minsize(500, 400)
# Makes the window grid cells resizable in this manner:
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)


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


def create_welcome_message() -> None:
    """
    Welcome message for the chat log
    """
    exit_words = EXIT_KEYWORDS
    msg = 'Welcome! My name is CopyCat. '
    msg += 'Enter any of the following to quit: '
    msg += f'{arr_to_string(exit_words)}.\n\n\n'
    # May edit later...

    chat_log.insert(tk.END, msg)
    # Do not want user to be able to type in log
    chat_log.config(state=tk.DISABLED)


create_welcome_message()


PLACEHOLDER_TEXT = "Type your message here..."


def add_placeholder(event=None) -> None:  # pylint: disable=unused-argument
    """
    Adds placeholder text if the input box is empty
    """
    if not input_area.get("1.0", tk.END).strip():
        input_area.insert("1.0", PLACEHOLDER_TEXT)


def remove_placeholder(event=None) -> None:  # pylint: disable=unused-argument
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
    input_box = tk.Text(window, width=40, height=4,
                        padx=5, pady=5, wrap=tk.WORD,
                        relief=tk.FLAT, bd=5, highlightbackground="white",
                        highlightthickness=2)
    input_box.grid(row=1, rowspan=2,
                   column=0, padx=10, pady=10, sticky='ew')

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
    send.grid(row=2, column=1, padx=10, pady=10)
    return input_box


input_area = create_user_input_area()
input_area.bind("<Return>", show_response)  # Enter/Return to send


def update_message_counter():
    """
    Message counter box
    """
    message_counter_box = tk.Text(window, width=16 + len(str(MSG_COUNTER)),
                                  height=1, wrap=tk.WORD, relief=tk.FLAT, bd=5,
                                  highlightbackground="white",
                                  highlightthickness=2)
    message_counter_box.grid(row=1, column=1)
    msg = f'Messages sent: {MSG_COUNTER}'
    message_counter_box.config(state=tk.NORMAL)
    message_counter_box.insert("1.0", msg)
    message_counter_box.config(state=tk.DISABLED)


update_message_counter()


def display_information():
    """
    Information displaying frame
    """
    display_text = "CopyCat is a program that will simply repeat what you say "
    display_text += "until the end of time (or your battery is drained), "
    display_text += "nothing too impressive, just a small project I wanted "
    display_text += "to work on to brush up on my Tkinter skills."

    root = tk.Tk()
    root.resizable(False, False)
    root.title("Additional Information")
    info_box = tk.Text(root, bd=20, relief=tk.FLAT, wrap=tk.WORD,
                       highlightbackground="white", highlightthickness=3,
                       height=4, width=len(display_text) // 5 + 13)  # Clean
    info_box.insert(tk.END, display_text)
    info_box.pack()
    info_box.config(state=tk.DISABLED)


def create_menu():
    """
    Creates the menu.
    """
    menubar = tk.Menu(window)
    options = tk.Menu(menubar, tearoff=0)
    info = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='CopyCat', menu=info)
    menubar.add_cascade(label='Options', menu=options)
    options.add_command(label='Toggle shouting feature', command=toggle_shout)
    info.add_command(label='Additional Information',
                     command=display_information)
    window.config(menu=menubar)


create_menu()
# Start the UI event loop
window.mainloop()
