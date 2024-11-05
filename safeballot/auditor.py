import sqlite3
from config import load_contract

class Auditor:
    def __init__(self, auditor_id, contract):
        self.auditor_id = auditor_id
        self.contract = contract

    def login(self):
        # Auditor login check from SQLite database
        conn = sqlite3.connect('database/voting_system.db')
        print("Conn:", conn) 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auditors WHERE auditor_id=?", (self.auditor_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def pull_voting_statistics(self, candidate_id):
        # Retrieves vote count for a specific candidate from the blockchain
        vote_count = self.contract.functions.getVoteCount(candidate_id).call()
        print(f"Candidate {candidate_id} has {vote_count} votes.")
        return vote_count

    def approve_election(self, election_id):
        # Marks an election as approved in the local database
        conn = sqlite3.connect('database/voting_system.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE elections SET is_approved=1 WHERE election_id=?
        """, (election_id,))
        conn.commit()
        conn.close()
        print(f"Election ID {election_id} has been approved.")
