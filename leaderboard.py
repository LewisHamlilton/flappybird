import tkinter as tk
from tkinter import ttk
import pymysql

class ScoreCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaderboard")
        self.root.geometry("500x400")
        self.root.configure(bg="white")
        
        # Title Label
        self.title_label = tk.Label(root, text="LEADERBOARD", font=("Arial", 24, "bold"), bg="white", fg="darkblue")
        self.title_label.pack(pady=10)
        
        # Create a Treeview widget
        self.tree = ttk.Treeview(root, columns=("Rank", "Player Name", "High Score"), show='headings')

        # Define the column headings
        self.tree.heading("Rank", text="Rank")
        self.tree.heading("Player Name", text="Player Name")
        self.tree.heading("High Score", text="High Score")

        # Set column widths
        self.tree.column("Rank", width=50, anchor="center")
        self.tree.column("Player Name", width=150, anchor="center")
        self.tree.column("High Score", width=100, anchor="center")

        # Style the Treeview
        style = ttk.Style()
        style.configure("Treeview", background="lightblue", foreground="black", rowheight=25, font=('Arial', 10))
        style.configure("Treeview.Heading", background="red", foreground="white", font=('Arial', 12, 'bold'))
        style.map("Treeview", background=[('selected', 'lightgreen')])
        
        # Fetch and insert data
        self.fetch_data()
        
        # Pack the Treeview widget
        self.tree.pack(pady=10)
        
        # Home Button
        self.home_button = tk.Button(root, text="Home", font=("Arial", 14), command=self.go_home, bg="lightgray", fg="black")
        self.home_button.pack(pady=10)

    def fetch_data(self):
        try:
            # Connect to MySQL database
            con = pymysql.connect(host="localhost", user="root", password="aditya", database="userdatu")
            cursor = con.cursor()

            # Fetch high scores sorted in descending order
            cursor.execute("SELECT username, high_score FROM data ORDER BY high_score DESC")
            rows = cursor.fetchall()
            con.close()

            # Insert data into the leaderboard
            for idx, (username, high_score) in enumerate(rows, start=1):
                self.tree.insert("", "end", values=(idx, username, high_score))

        except Exception as e:
            print("Database Error:", e)

    def go_home(self):
        self.root.destroy()  # Closes the leaderboard window

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreCardApp(root)
    root.mainloop()
