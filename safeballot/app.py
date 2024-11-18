# File: app.py
# Purpose: This file contains the Flask application for the voting system.
#  It manages routes for logging in different user roles (admin, auditor, voter), creating elections, viewing current elections, managing voter registration, and handling sessions for users.
# Authors: Ella Brink, Lauren Wilson, Emma Bellai, Lucy DiSalvo
# Version History:
# - Version 1.0 (Sprint 2): Initial version created by Ella Brink
# - Version 1.1 (Sprint 2): Fixed Admin login bug, Admin using 'adminid' can now sign in by Lucy DiSalvo
# - Version 1.2 (Sprint 3): Fixed Voter login, voters saved in database can now log in by Lucy DiSalvo 
# - Version 1.3 (Sprint 4): Added reroute to /view_electionsAu for auditor user by Lucy DiSalvo 
# - Version 1.4 (Sprint 4): Added reroute to /view_elections_voter for voter user by Ella Brink 
# - Version 1.5 (Sprint 4): Revise reroute to /admin_dashboard for auditor user by Ella Brink
# - Version 1.6 (Sprint 4): Added /cast_vote route by Ella Brink
# - Version 1.7 (Sprint 4): Added /submit_vote, revised /view_elections_admin, update database imports by Ella Brink
# - Version 1.8 (Sprint 4): Updated blockchain logic, created contract_address, provider_url and contract_abit for ganache integration by Lucy DiSalvo
# - Version 1.9 (Sprint 4): Added flash messages for signup success and failure by Lauren Wilson
# - Version 2.0 (Sprint 4): Flashed error messages for both duplicate SSN or driver ID by Lauren Wilson
# - Version 2.1 (Sprint 4): Harcoded auditorid by Lauren Wilson
# - Version 2.2 (Sprint 4): Fixed voter login by Lauren Wilson
# - Version 2.3 (Sprint 4): Added close election function by Lauren Wilson


from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import add_voter, add_vote, get_voter, get_candidates, tally_votes, create_candidates_table, create_election, get_current_elections, create_database, create_elections_table, get_all_voters, create_votes_table, close_election_in_db
from voter import Voter
from web3 import Web3
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'cis454'  # Set a secret key for session management

# Pre-defined admin ID (for demonstration purposes, use a secure method in production)
ADMIN_ID = 'adminid'  # Replace with your actual admin ID
AUDITOR_ID = 'auditorid'

provider_url = 'http://localhost:7545'  # Example for Ganache
contract_address = '0x2AeFE84084b722a89C90fADee9C39Db9CE37055e'  # Replace with your actual contract address
contract_abi = [{
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "candidates",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "voteCount",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [],
      "name": "candidatesCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "voters",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function",
      "constant": True
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        }
      ],
      "name": "addCandidate",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "candidateId",
          "type": "uint256"
        }
      ],
      "name": "vote",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }]


# Home route
@app.route('/')
def index():
    return render_template('index.html')  # Render the home page template

# Login route for voters, admins, and auditors
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']  # Get user role from form
        print(f"Role selected: {role}")

        #LOGIN OPTIONS
        if role == 'admin':
            user_id = request.form['user_id']  # Get user ID from form
            if user_id == ADMIN_ID:  # Validate admin ID
                session['admin_name'] = user_id  # Store admin name in session
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
            else:
                flash("Invalid admin ID, please try again.", "error")  # Flash error message
                return redirect(url_for('login'))  # Redirect back to login page

        elif role == 'auditor':
            u_id = request.form['u_id']  # Get user ID from form
            if u_id == AUDITOR_ID:
              session['auditor_name'] = u_id  # Store auditor name in session
              return redirect(url_for('auditor_dashboard'))  # Redirect to auditor dashboard
            else:
                flash("Invalid auditor ID, please try again.", "error")  # Flash error message
                return redirect(url_for('login'))  # Redirect back to login page

        elif role == 'voter':
            ssn = request.form['ssn'] 
            zipcode = request.form['zipcode']
            driver_id = request.form['driver_id'] 
            print(f"SSN received: {ssn}") 
            print(f"Zipcode received: {zipcode}")
            print(f"Driver ID received: {driver_id}")

            voter_info = get_voter(ssn)
            print(f"Debug: get_voter returned: {voter_info}")

            if not voter_info:
                flash("Voter not found. Please check your credentials.", "error")
                return redirect(url_for('login'))
            
            if voter_info[2] == ssn and voter_info[3] == zipcode and voter_info[4] == driver_id:
                session['voter_id'] = voter_info[0]
                flash('Signup successful! You can now log in.', 'success')
                return redirect(url_for('voter_dashboard'))
            else:
                flash("Invalid voter credentials. Please try again.", "error")
                return redirect(url_for('login'))

    return render_template('login.html')


# Admin dashboard route
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_name' not in session:
        flash("Please log in as an admin.", "error")
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name', '').strip()
        date = request.form.get('date', '').strip()
        candidate1 = request.form.get('candidate1', '').strip()
        candidate2 = request.form.get('candidate2', '').strip()
        candidate3 = request.form.get('candidate3', '').strip()
        candidate4 = request.form.get('candidate4', '').strip()

        # Validate required fields
        if not name or not date or not candidate1 or not candidate2:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for('admin_dashboard'))
        # Parse the date in MM/DD/YYYY format to a datetime.date object
        date = date.strip()
        # Parse the date in MM/DD/YYYY format to a datetime.date object
        election_date = datetime.strptime(date, '%Y-%m-%d').date()
    
        # Compare the parsed date with today's date
        if election_date < datetime.now().date():
            flash("Election date cannot be in the past. Please select a future date.", "error")
            return redirect(url_for('admin_dashboard'))
      
        # Fetch current elections
        current_elections = get_current_elections()
        if not current_elections:
            flash("Failed to retrieve current elections. Please try again later.", "error")
            return redirect(url_for('admin_dashboard'))

        # Check for duplicate election names
        existing_names = {election['name'].strip().lower() for election in current_elections}
        if name.lower() in existing_names:
            flash("An election with this name already exists. Please choose a different name.", "error")
            return redirect(url_for('admin_dashboard'))

        # Create a new election
        # Use the normalized date (YYYY-MM-DD) for database insertion
        election_id = create_election(name, election_date.strftime('%Y-%m-%d'), candidate1, candidate2, candidate3, candidate4)
        if election_id:  # Assuming create_election returns an ID if successful
            flash("Election created successfully!", "success")
        else:
            flash("Failed to create the election. Please try again.", "error")

        return redirect(url_for('admin_dashboard'))

    return render_template('admin_dashboard.html', admin_name=session.get('admin_name'))


#view election for admin 
@app.route('/view_elections')
def view_elections():
    if 'admin_name' in session:
        elections = get_current_elections()  # Fetch current elections with candidates
        return render_template('view_elections.html', elections=elections)
    else:
        flash("You need to log in as admin first.", "error")
        return redirect(url_for('login'))
    

#Auditor view of elections
@app.route('/view_electionsAu')
def view_elections_auditor():
    elections = get_current_elections()  # Fetch current elections from the database
    return render_template('view_electionsAu.html', elections=elections)  # Render the view elections page


@app.route('/close_election/<int:election_id>', methods=['POST'])
def close_election(election_id):
    close_election_in_db(election_id)
    flash('Election closed successfully.', 'success')
    return redirect(url_for('view_elections_auditor'))

# Auditor dashboard route
@app.route('/auditor_dashboard')
def auditor_dashboard():
    return render_template('auditor_dashboard.html', auditor_name=session.get('auditor_name'))  # Render the auditor dashboard template

# Voter dashboard route
@app.route('/voter_dashboard')
def voter_dashboard():
    return render_template('voter_dashboard.html')  # Render the voter dashboard template

@app.route('/view_elections_voter')
def view_elections_voter():
    elections = get_current_elections() 
    return render_template('view_elections_voter.html', elections=elections)

# Signup route for new voters
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        ssn = request.form['ssn']
        zipcode = request.form['zipcode']
        driver_id = request.form['driver_id']
        
        if add_voter(ssn, zipcode, driver_id):
            flash('Signup successful! You can now log in.', 'success')  # Flash success message
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        else:
            flash("Voter with this SSN or Driver ID already exists.", "error")  # Error message
            return redirect(url_for('signup'))  # Redirect back to signup page

    return render_template('signup.html')  # Render the signup page

#cast vote
@app.route('/cast/<int:election_id>', methods=['GET', 'POST'])
def cast(election_id):
    elections = get_current_elections()

    election = next((e for e in elections if e['id'] == election_id), None)

    if not election:
        flash("Election not found.", "error")
        return redirect(url_for('view_elections_voter'))

    if request.method == 'POST':
        selected_candidate_id = request.form['candidate_id']
        voter_id = session.get('voter_id')
        
        if voter_id:
            add_vote(voter_id, selected_candidate_id, election_id)
            return render_template('successful_vote.html')
        else:
            flash("Please log in to vote.", "error")
            return redirect(url_for('login'))

    # Fetch candidates from the candidates table based on election_id
    candidates = get_candidates(election_id) 
    return render_template('cast.html', election_title=election['name'], candidates=candidates, election_id=election_id)

@app.route('/successful_vote') 
def successful_vote(): 
  return render_template('successful_vote.html')

@app.route('/statistics/<int:election_id>', methods=['GET'])
def statistics(election_id):
  candidates, election = tally_votes(election_id)

    # Calculate time left in the election

  return render_template('statistics.html', candidates=candidates, election=election)


# Logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Clear session data
    return render_template('logout.html')  # Render logout.html after logging out

# Run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

for rule in app.url_map.iter_rules():
    print(rule) 

