import sqlite3
from config import load_contract

class Admin:
    def __init__(self, admin_id, contract):
        self.admin_id = admin_id
        self.contract = contract

    def login(self):
        # Admin login check from SQLite database
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE admin_id=?", (self.admin_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def create_election(self, title, start_time, end_time):
        # Inserts a new election into the database
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO elections (title, start_time, end_time, is_active) 
            VALUES (?, ?, ?, 1)
        """, (title, start_time, end_time))
        conn.commit()
        conn.close()
        print(f"Election '{title}' created successfully.")

    def post_results(self, candidate_id):
        # Retrieves total votes for a candidate from the blockchain
        vote_count = self.contract.functions.getVoteCount(candidate_id).call()
        print(f"Total votes for candidate {candidate_id}: {vote_count}")
        # Additional functionality to log or update results can be added here
