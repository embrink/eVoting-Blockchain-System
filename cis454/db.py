import sqlite3

def create_connection(db_file):
    connect = sqlite3.connect(db_file)
    return connect

def initialize_db(connect):
    cursor = connect.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')
    
    # Create elections table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS elections (
        election_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        start_date DATE,
        end_date DATE,
        status TEXT
    )
    ''')
    
    # Create candidates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        election_id INTEGER,
        name TEXT,
        FOREIGN KEY (election_id) REFERENCES elections(election_id)
    )
    ''')

    # Create votes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
        election_id INTEGER,
        user_id INTEGER,
        candidate_id INTEGER,
        FOREIGN KEY (election_id) REFERENCES elections(election_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
        UNIQUE(user_id, election_id)
    )
    ''')

    # Create results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        result_id INTEGER PRIMARY KEY AUTOINCREMENT,
        election_id INTEGER,
        candidate_id INTEGER,
        vote_count INTEGER,
        FOREIGN KEY (election_id) REFERENCES elections(election_id),
        FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
    )
    ''')

    connect.commit()
