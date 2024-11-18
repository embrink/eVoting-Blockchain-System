# File: database.py
# Purpose: This file contains functions to manage voters and elections within a SQLite-based voting system.
# It includes functionality for adding voters, retrieving voter information, creating elections, and managing the database schema.
# Authors: 
# Version History:
# - Version 1.0 (Sprint 3): Initial version created by Ella Brink
# - Version 1.1 (Sprint 3): Fixed create elections bug, Elections now displayed on webpage by Lauren Wilson
# - Version 1.2 (Sprint 3): Voters now stored correctly in database after signing up by Lucy DiSalvo 
# - Version 1.3 (Sprint 3): Manually add voters to database and print statements for testing by Lucy DiSalvo 
# - Version 1.4 (Sprint 4): Added documentation by Lucy DiSalvo 
# - Version 1.5 (Sprint 4): Revise Database to include Candidates by Ella Brink
# - Version 1.6 (Sprint 4): Added create_election_table, get_current_elections by Ella Brink
# - Version 1.6.1 (Sprint 4): Modified create_election_table, create_election, create_candidate_table, added add_candidate function by Ella Brink
# - Version 1.7 (Sprint 4): Modified database to hold candidates and correctly populate by Ella Brink
# - Version 1.8 (Sprint 4): Made driver's license ID requirement unique, eliminated duplicated IDs by Lauren Wilson
# - Version 1.9 (Sprint 4): Added Close Election Function by Lauren Wilson




import sqlite3
import uuid  # For generating unique voter IDs


def create_connection():
    conn = sqlite3.connect('voting_system.db')
    return conn

def add_voter(ssn, zipcode, driver_id):
    print(f"Attempting to add voter: SSN={ssn}, Zipcode={zipcode}, Driver ID={driver_id}")
    
    # Generate a unique voter ID
    voter_id = str(uuid.uuid4())  
    
    # Check if the SSN or driver's license is already in use
    if get_voter(ssn):
        print(f"SSN {ssn} already exists in the database.")
        return None
    if get_voter_by_driverid(driver_id):
        print(f"Driver ID {driver_id} already exists in the database.")
        return None

    # Create a new connection for the insert operation
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # Insert the new voter record into the database
        cursor.execute('''
            INSERT INTO voters (voter_id, ssn, zipcode, driver_id)
            VALUES (?, ?, ?, ?)
        ''', (voter_id, ssn, zipcode, driver_id))
        conn.commit()  # Commit the changes to the database
        print(f"Voter added successfully: {voter_id}")  # Debugging output
        return voter_id  # Return the generated voter ID
    except sqlite3.IntegrityError:
        # Handle case where SSN or Driver ID is a duplicate
        print(f"Error: SSN {ssn} or Driver ID {driver_id} already exists.")
        return None
    finally:
        # Close the database connection
        conn.close()


def get_voter(ssn):
    """Check if a voter already exists by SSN."""
    conn = create_connection()
    if conn is None:
        print("Error! cannot create the database connection.")
        return None
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voters WHERE ssn = ?', (ssn,))
    voter = cursor.fetchone()
    if voter:
        print(f"Debug: Voter found: {voter}")
    else:
        print("Debug: No voter found with that SSN.")
    conn.close()
    return voter

def get_voter_by_driverid(driver_id):
    """Check if a voter already exists by driver ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voters WHERE driver_id = ?', (driver_id,))
    voter = cursor.fetchone()
    conn.close()
    return voter


# Call this function once to create the database and table of VOTERS
def create_database():
    """Create the database and the voters table if it doesn't exist."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT NOT NULL UNIQUE,  -- Added voter_id column
            ssn TEXT NOT NULL UNIQUE,
            zipcode TEXT NOT NULL,
            driver_id TEXT NOT NULL UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
#create database
def create_elections_table():
    """Create elections table with up to 4 candidate columns."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elections (
                election_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                candidate1 TEXT,
                candidate2 TEXT,
                candidate3 TEXT,
                candidate4 TEXT,
                status TEXT DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
create_elections_table()

#table with candidates and random ID
def create_candidates_table():
    """Create candidates table with a unique ID and name."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
                election_id INTEGER NOT NULL,
                vote_count INTEGER DEFAULT 0,
                name TEXT NOT NULL,
                FOREIGN KEY (election_id) REFERENCES elections (election_id)
            )
        ''')
        conn.commit()

create_candidates_table()

def get_candidates(election_id):
    """Fetch candidates by election_id from the candidates table."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT candidate_id, name FROM candidates WHERE election_id = ?', (election_id,))
        candidates = cursor.fetchall()
    return candidates


def create_votes_table():
    """Create votes table to store voter, candidate, and election IDs along with vote counts."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id INTEGER NOT NULL,
                candidate_id INTEGER NOT NULL,
                election_id INTEGER NOT NULL,
                FOREIGN KEY(voter_id) REFERENCES voters(id),
                FOREIGN KEY(candidate_id) REFERENCES candidates(id),
                FOREIGN KEY(election_id) REFERENCES elections(election_id)
            )
        ''')
        conn.commit()

create_votes_table()

def add_vote(voter_id, candidate_id, election_id, vote_count=1):
    """Add a vote to the votes table and update vote counts in both votes and candidates tables."""
    with create_connection() as conn:
        cursor = conn.cursor()
        
        # Insert the vote into the votes table
        cursor.execute('''
            INSERT INTO votes (voter_id, candidate_id, election_id)
            VALUES (?, ?, ?)
        ''', (voter_id, candidate_id, election_id))
        
        # Increment the vote count in the votes table (if necessary)
        cursor.execute('''
            UPDATE candidates
            SET vote_count = vote_count + ?
            WHERE candidate_id = ? AND election_id = ?
        ''', (vote_count, candidate_id, election_id))
        
        conn.commit()

def tally_votes(election_id):
    """Fetch the total votes for each candidate in a specific election and the election details."""
    with create_connection() as conn:
        cursor = conn.cursor()

        # Get election details
        elections = get_current_elections()
        election = next((e for e in elections if e['id'] == election_id), None)
        if not election:
            return [], None

        # Get candidate names and their vote counts
        cursor.execute('''
            SELECT name, vote_count
            FROM candidates
            WHERE election_id = ?
        ''', (election_id,))
        candidates = cursor.fetchall()
    return candidates, election


        
# Add an election with candidates as separate arguments
def create_election(name, date, candidate1, candidate2, candidate3=None, candidate4=None):
    """Insert a new election with up to 4 candidates, setting None for any missing candidates."""
    with create_connection() as conn:
        cursor = conn.cursor()

        # Set candidate3 and candidate4 to None if they are empty strings (HERE)
        candidate3 = candidate3 if candidate3 else None
        candidate4 = candidate4 if candidate4 else None

        # Insert the election
        cursor.execute('''
            INSERT INTO elections (name, date, candidate1, candidate2, candidate3, candidate4, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, date, candidate1, candidate2, candidate3, candidate4, 'active'))
        # Get the ID of the last inserted row (election_id)
        election_id = cursor.lastrowid 
        # Add candidates to the candidates table
        candidate_ids = []
        for candidate in [candidate1, candidate2, candidate3, candidate4]:
            if candidate:
                cursor.execute('''
                    INSERT INTO candidates (name, election_id)
                    VALUES (?, ?)
                ''', (candidate, election_id))
                candidate_ids.append(cursor.lastrowid)
        conn.commit()
        print(f"Election created with ID: {election_id}")
        return election_id

def get_current_elections():
    # Use 'with' to automatically handle closing the connection
    with create_connection() as conn:
        cursor = conn.cursor()
        # Fetch all columns for each election where status is 'active'
        cursor.execute("SELECT * FROM elections WHERE status = 'active'")
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        elections = [
            {
                'id': row[0],
                'name': row[1],
                'date': row[2],
                'candidate1': row[3],
                'candidate2': row[4],
                'candidate3': row[5],
                'candidate4': row[6],
                'status': row[7],
                'created_at': row[8]
            }
            for row in rows
        ]
    # Return the elections list after closing the connection (handled by 'with')
    return elections

def close_election_in_db(election_id):
    """Mark an election as closed in the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE elections SET status = "closed" WHERE election_id = ?', (election_id,))
    conn.commit()
    conn.close()




def get_all_voters():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM voters')
    voters = cursor.fetchall()  # Fetch all records from the voters table
    conn.close()
    return voters

add_voter('123-45-6789', '12345', 'D1234567')  # Example test data
add_voter('987-65-4321', '54321', 'D7654321') #ssn, zipcode, driver id 
