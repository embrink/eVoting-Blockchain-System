from models import connect

def cast_vote(user_id, election_id, candidate_id):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO votes (election_id, user_id, candidate_id) VALUES (?, ?, ?)", 
                   (election_id, user_id, candidate_id))
    connect.commit()
    print("Vote cast successfully.")
