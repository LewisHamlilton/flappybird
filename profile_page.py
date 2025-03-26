import sys
import tkinter as tk
from tkinter import Label

def show_profile(username):
    root = tk.Tk()
    root.title("User Profile")
    root.geometry("300x200")

    label = Label(root, text=f"Welcome, {username}!", font=("Arial", 14))
    label.pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]  # Fetch username from argument
        show_profile(username)
    else:
        print("No username provided!")
