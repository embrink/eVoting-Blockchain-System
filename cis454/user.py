import sqlite3

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect('voting_system.db')
    return conn

def register_user(username, password, role):
    """Register a new user with a specific role."""
    conn = create_connection()
    cursor = conn.cursor()
    
    # Check if username already exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
    if cursor.fetchone()[0] > 0:
        print("Error: Username already exists.")
        conn.close()
        return False

    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()
    return True

def login(username, password):
    """Log in a user and return their user ID and role."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns (user_id, role) or None if not found

def get_user_role(user_id):
    """Get the role of a user by their user ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    role = cursor.fetchone()
    conn.close()
    return role[0] if role else None

def change_password(user_id, new_password):
    """Change the password of a user."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()

def view_users():
    """Admin function to view all registered users."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    """Admin function to delete a user."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
