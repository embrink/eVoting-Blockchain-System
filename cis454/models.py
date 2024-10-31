from db import create_connection, initialize_db

DB_FILE = "voter_database.db"

# Create a global connection
conn = create_connection(DB_FILE)
initialize_db(conn)

def insert_user(username, password, role):
    """Insert a new user into the database."""
    cursor = conn.cursor()
    
    # Check if the username already exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
    if cursor.fetchone()[0] > 0:
        print("Error: Username already exists.")
        return False

    # Insert the new user
    cursor.execute('''
    INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    ''', (username, password, role))
    conn.commit()
    print("User registered successfully.")
    return True

def get_user(username, password):
    """Retrieve a user from the database by username and password."""
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, role FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    if user:
        return user  # Returns user ID and role if successful
    else:
        print("Error: Invalid username or password.")
        return None  # Returns None if no match found

def get_all_users():
    """Retrieve all users from the database (for admin purposes)."""
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, role FROM users")
