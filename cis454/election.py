# election.py
from models import conn

def create_election(name, start_date, end_date):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO elections (name, start_date, end_date, status) VALUES (?, ?, ?, 'active')", 
                   (name, start_date, end_date))
    conn.commit()
    print("Election created successfully.")

def get_active_elections():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM elections WHERE status='active'")
    return cursor.fetchall()
