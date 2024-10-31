from models import connect

def view_election_statistics(election_id):
    conn = connect()  # Call the connect function to get a connection object
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM votes WHERE election_id=?", (election_id,))
    total_votes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='voter'")
    total_voters = cursor.fetchone()[0]

    print(f"Total Voters: {total_voters}, Total Votes: {total_votes}")
    if total_votes > total_voters:
        print("Error: Number of votes exceeds number of voters!")
    else:
        print("Election statistics verified.")

    conn.close()  # Close the connection
