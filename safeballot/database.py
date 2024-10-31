import sqlite3
import uuid  # For generating unique voter IDs

def create_connection():
    conn = sqlite3.connect('voting_system.db')
    return conn

def add_voter(ssn, zipcode, driver_id):
    voter_id = str(uuid.uuid4())  # Generate a unique voter ID
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO voters (voter_id, ssn, zipcode, driver_id)
            VALUES (?, ?, ?, ?)
        ''', (voter_id, ssn, zipcode, driver_id))
        conn.commit()
        return voter_id  # Return the generated voter ID
    except sqlite3.IntegrityError:
        # This error occurs if the SSN is already in the database
        return None
    finally:
        conn.close()

def get_voter(ssn):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT voter_id, zipcode, driver_id FROM voters WHERE ssn = ?', (ssn,))
    voter = cursor.fetchone()
    conn.close()
    return voter

# Call this function once to create the database and table
def create_database():
    conn = create_connection()
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
    conn.close()

create_database()  # Create the database and table if it doesn't exist
def create_election(name, date):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO elections (name, date, status)
        VALUES (?, ?, ?)
    ''', (name, date, 'Open'))  # Setting the initial status to 'Open'
    
    conn.commit()
    conn.close()

def get_current_elections():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, date, status FROM elections')
    elections = cursor.fetchall()
    
    conn.close()
    return [{'name': row[0], 'date': row[1], 'status': row[2]} for row in elections]

# Call this function once to create the elections table
def create_elections_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS elections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

create_elections_table() 