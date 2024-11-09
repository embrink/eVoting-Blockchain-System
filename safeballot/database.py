import sqlite3
import uuid  # For generating unique voter IDs

def create_connection():
    conn = sqlite3.connect('voting_system.db')
    return conn

def add_voter(ssn, zipcode, driver_id):
    print(f"Attempting to add voter: SSN={ssn}, Zipcode={zipcode}, Driver ID={driver_id}")
    voter_id = str(uuid.uuid4())  # Generate a unique voter ID
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO voters (voter_id, ssn, zipcode, driver_id)
            VALUES (?, ?, ?, ?)
        ''', (voter_id, ssn, zipcode, driver_id))
        conn.commit()
        print(f"Voter added successfully: {voter_id}")  # Debugging
        return voter_id  # Return the generated voter ID
    except sqlite3.IntegrityError:
        # This error occurs if the SSN is already in the database
        return None
    finally:
        conn.close()

def get_voter(ssn):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT voter_id, ssn, zipcode, driver_id FROM voters WHERE ssn = ?', (ssn,))
    voter = cursor.fetchone()
    print(f"Query result for SSN {ssn}: {voter}") #debugging statement 
    conn.close()
    return voter

# Call this function once to create the database and table
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
            driver_id TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
# update status for election to pull : ella 11/9
def create_election(name, date, candidates):
    """Insert a new election into the elections table."""
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO elections (title, start_time, end_time, candidates, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, date, date, candidates, 1))  # Make sure the date is used correctly
        conn.commit()
        # Get the ID of the last inserted row (election_id)
        election_id = cursor.lastrowid
    return election_id

#get election based off status : ella 11/9
def get_current_elections():
    """Get all the current elections (optionally filter by 'Open' status)."""
    with create_connection() as conn:
        cursor = conn.cursor()
        #cursor.execute('SELECT id, name, date, status FROM elections WHERE status = ?', ('Open',))  # Fetch only 'Open' elections
        cursor.execute('SELECT id, name, date, status FROM elections') 
        elections = cursor.fetchall()
    return [{'id': row[0], 'name': row[1], 'date': row[2], 'status': row[3]} for row in elections]

def create_elections_table():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elections (
                election_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                candidates TEXT NOT NULL,  -- Ensure this column exists
                is_active INTEGER DEFAULT 1
            );
        ''')
        conn.commit()


create_elections_table() 


def get_all_voters():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM voters')
    voters = cursor.fetchall()  # Fetch all records from the voters table
    conn.close()
    return voters

add_voter('123-45-6789', '12345', 'D1234567')  # Example test data
add_voter('987-65-4321', '54321', 'D7654321') #ssn, zipcode, driver id 