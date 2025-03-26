import tkinter as tk
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
        self.root.geometry("400x300")
        self.root.configure(bg="white")
        
        # ✅ Display Username at the top
        tk.Label(root, text=f"Welcome, {username}!", font=("Arial", 14, "bold"), bg="white", fg="green").pack(pady=10)

        # Title Label
        tk.Label(root, text="🎮 Main Menu 🎮", font=("Arial", 18, "bold"), bg="white", fg="darkblue").pack(pady=10)
        
        # Play Game Button
        play_button = tk.Button(root, text="Play Game", font=("Arial", 14), command=self.play_game, bg="lightblue", fg="black")
        play_button.pack(pady=10)

        # Leaderboard Button
        leaderboard_button = tk.Button(root, text="Leaderboard", font=("Arial", 14), command=self.open_leaderboard, bg="lightblue", fg="black")
        leaderboard_button.pack(pady=10)

        # Logout Button
        logout_button = tk.Button(root, text="Logout", font=("Arial", 14), command=self.logout, bg="red", fg="white")
        logout_button.pack(pady=10)

    def play_game(self):
        # ✅ Pass the username to display_selections.py
        subprocess.Popen(["python", "display_selections.py", username])

    def open_leaderboard(self):
        subprocess.Popen(["python", "leaderboard.py"])

    def logout(self):
        self.root.destroy()
        subprocess.run(["python", "signin.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
