import tkinter as tk
from tkinter import messagebox, simpledialog
from user import register_user, login
from election import create_election, get_active_elections
from voting import cast_vote
from audit import view_election_statistics

class VotingSystemApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voting System")
        
        self.role = None
        self.user_id = None

        # Main menu
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(pady=20)

        self.label_username = tk.Label(self.main_frame, text="Username:")
        self.label_username.grid(row=0, column=0)
        self.entry_username = tk.Entry(self.main_frame)
        self.entry_username.grid(row=0, column=1)

        self.label_password = tk.Label(self.main_frame, text="Password:")
        self.label_password.grid(row=1, column=0)
        self.entry_password = tk.Entry(self.main_frame, show="*")
        self.entry_password.grid(row=1, column=1)

        self.button_login = tk.Button(self.main_frame, text="Login", command=self.login_user)
        self.button_login.grid(row=2, columnspan=2, pady=10)

        self.button_register = tk.Button(self.main_frame, text="Register", command=self.register_user)
        self.button_register.grid(row=3, columnspan=2, pady=5)

    def register_user(self):
        username = simpledialog.askstring("Register", "Enter username:")
        password = simpledialog.askstring("Register", "Enter password:")
        role = simpledialog.askstring("Register", "Enter role (voter/admin/auditor):")
        try:
            register_user(username, password, role)
            messagebox.showinfo("Success", "User registered successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        user_info = login(username, password)
        
        if user_info:
            self.user_id, self.role = user_info
            messagebox.showinfo("Success", f"Logged in as {self.role}.")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def show_dashboard(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Create role-specific dashboard
        if self.role == 'voter':
            self.create_voter_dashboard()
        elif self.role == 'admin':
            self.create_admin_dashboard()
        elif self.role == 'auditor':
            self.create_auditor_dashboard()

    def create_voter_dashboard(self):
        tk.Label(self.main_frame, text="Voter Dashboard").pack(pady=10)
        
        tk.Button(self.main_frame, text="View Active Elections", command=self.view_active_elections).pack(pady=5)
        tk.Button(self.main_frame, text="Cast Vote", command=self.cast_vote).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def create_admin_dashboard(self):
        tk.Label(self.main_frame, text="Admin Dashboard").pack(pady=10)
        
        tk.Button(self.main_frame, text="Create Election", command=self.create_election).pack(pady=5)
        tk.Button(self.main_frame, text="Post Results", command=self.post_results).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def create_auditor_dashboard(self):
        tk.Label(self.main_frame, text="Auditor Dashboard").pack(pady=10)
        
        tk.Button(self.main_frame, text="View Election Statistics", command=self.view_statistics).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=5)

    def view_active_elections(self):
        elections = get_active_elections()
        elections_str = "\n".join([f"ID: {e[0]}, Name: {e[1]}" for e in elections])
        messagebox.showinfo("Active Elections", elections_str)

    def cast_vote(self):
        election_id = simpledialog.askstring("Vote", "Enter election ID to vote in:")
        candidate_id = simpledialog.askstring("Vote", "Enter candidate ID to vote for:")
        cast_vote(self.user_id, election_id, candidate_id)
        messagebox.showinfo("Success", "Vote cast successfully.")

    def create_election(self):
        name = simpledialog.askstring("Create Election", "Enter election name:")
        start_date = simpledialog.askstring("Create Election", "Enter start date (YYYY-MM-DD):")
        end_date = simpledialog.askstring("Create Election", "Enter end date (YYYY-MM-DD):")
        create_election(name, start_date, end_date)
        messagebox.showinfo("Success", "Election created successfully.")

    def post_results(self):
        # Add functionality to post results
        messagebox.showinfo("Post Results", "Functionality not implemented yet.")

    def view_statistics(self):
        election_id = simpledialog.askstring("View Statistics", "Enter election ID:")
        statistics = view_election_statistics(election_id)
        messagebox.showinfo("Election Statistics", statistics)

    def logout(self):
        self.user_id = None
        self.role = None
        messagebox.showinfo("Logout", "Logged out successfully.")
        self.main_frame.destroy()
        self.__init__(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = VotingSystemApp(root)
    root.mainloop()
