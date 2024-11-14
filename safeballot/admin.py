
# File: admin.py
# Purpose: This file contains the Admin class which manages administrative functions in the voting system, including login, election creation, and posting election results. It interacts with the SQLite database for election management and a blockchain contract to retrieve election results.
# Authors: Ella Brink, Lauren Wilson, Emma Bellai, Lucy DiSalvo
# Version History:
# - Version 1.0 (Sprint 2): Initial version created by Ella Brink

import sqlite3
from config import load_contract
from database import create_connection  # Assuming create_connection is defined in database.py

class Admin:
    def __init__(self, admin_id, contract):
        self.admin_id = admin_id
        self.contract = contract

    def login(self):
        """Admin login check from SQLite database."""
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE admin_id=?", (self.admin_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def create_election(self, title, start_time, end_time, candidate_names):
        """Insert a new election and its candidates into the elections table."""
        with create_connection() as conn:
            cursor = conn.cursor()

            # Serialize the list of candidates as a comma-separated string
            candidates_str = ', '.join(candidate_names)  # or use json.dumps(candidate_names)

            # Insert election details into the elections table, including candidates
            cursor.execute('''
                INSERT INTO elections (title, start_time, end_time, candidates)
                VALUES (?, ?, ?, ?)
            ''', (title, start_time, end_time, candidates_str))

            conn.commit()
        print(f"Election '{title}' with candidates {candidates_str} created successfully.")

    def post_results(self, candidate_id):
        """Retrieve total votes for a candidate from the blockchain."""
        vote_count = self.contract.functions.getVoteCount(candidate_id).call()
        print(f"Total votes for candidate {candidate_id}: {vote_count}")
        # Additional functionality to log or update results can be added here
