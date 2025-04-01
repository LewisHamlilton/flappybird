import tkinter as tk
from PIL import Image, ImageTk  
import subprocess
import sys

# ✅ Get username from command-line argument
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "Player"  # Default if not provided

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("350x622")  # ✅ Set fixed window size
        
        # ✅ Load and set background image
        self.bg_image = Image.open("tree.jpg")
        self.bg_image = self.bg_image.resize((350, 622))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)
        
        # ✅ Display Username at the top with adjusted spacing
        tk.Label(root, text=f"Welcome, {username}!", font=("Arial", 14, "bold"), bg="white", fg="green").pack(pady=20)

        # ✅ Title Label placed slightly higher
        tk.Label(root, text="🎮 Main Menu 🎮", font=("Arial", 18, "bold"), bg="white", fg="darkblue").pack(pady=10)
        
        # ✅ Play Game Button positioned in the middle
        play_button = tk.Button(root, text="Play Game", font=("Arial", 14), command=self.play_game, bg="lightblue", fg="black")
        play_button.pack(pady=100)

        # ✅ Leaderboard Button slightly above logout
        leaderboard_button = tk.Button(root, text="Leaderboard", font=("Arial", 14), command=self.open_leaderboard, bg="lightblue", fg="black")
        leaderboard_button.pack(pady=20)

        # ✅ Logout Button positioned at the bottom
        logout_button = tk.Button(root, text="Logout", font=("Arial", 14), command=self.logout, bg="red", fg="white")
        logout_button.pack(side="bottom", pady=20)

    def play_game(self):
        # ✅ Pass the username to display_selections.py and destroy main menu
        self.root.destroy()
        subprocess.Popen(["python", "display_selections.py", username])

    def open_leaderboard(self):
        # ✅ Open the leaderboard and ensure the window size is the same
        self.root.geometry("350x622")
        leaderboard_process = subprocess.Popen(["python", "leaderboard.py"])
        self.root.withdraw()  # Hide main menu while leaderboard is open
        leaderboard_process.wait()  # ✅ Wait for leaderboard to close
        self.root.deiconify()  # Show main menu again

    def logout(self):
        self.root.destroy()
        subprocess.run(["python", "signin.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
