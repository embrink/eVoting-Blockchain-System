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
# - Version 1.8 (Sprint 4): Added flash messages for signup success and failure by Lauren wilson
# - Version 1.9 (Sprint 4): Flashed error messages for both duplicate SSN or driver ID by Lauren Wilson
# - Version 2.0 (Sprint 4): Harcoded auditorid by Lauren Wilson


from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import add_voter, get_voter, create_election, get_current_elections, create_database, create_elections_table, get_all_voters
from voter import Voter
from web3 import Web3


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
            ssn = request.form['ssn']          # Get SSN from form
            zipcode = request.form['zipcode']  # Get Zipcode from form
            driver_id = request.form['driver_id']  # Get Driver ID from form
            
            # Debugging statements
            print(f"SSN: {ssn}, Zipcode: {zipcode}, Driver ID: {driver_id}")

            # Validate voter credentials
            voter_info = get_voter(ssn)  # Get voter info based on SSN
            print(f"Get_voter info", voter_info) #debugging statement 
            
            if (voter_info[1] == ssn and voter_info[2] == zipcode and voter_info[3] == driver_id):
                session['voter_id'] = voter_info[0]  # Store voter ID in session
                return redirect(url_for('voter_dashboard'))  # Redirect to voter dashboard
            else:
                flash("Invalid voter credentials, please try again.", "error")  # Flash error message
                return redirect(url_for('login'))  # Redirect back to login page
        else:
            flash("Invalid role selected", "error")  # Flash error message
            return redirect(url_for('login'))  # Redirect back to login page
            
    return render_template('login.html')  # Render the login page template

# Admin dashboard route
@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin_name' not in session:
        flash("Please log in as an admin.", "error")
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        # Handle the form submission to create a new election
        name = request.form['name']
        date = request.form['date']
        
        # Retrieve each candidate individually
        candidate1 = request.form.get('candidate1')
        candidate2 = request.form.get('candidate2')
        candidate3 = request.form.get('candidate3', '')  # Optional, defaults to empty
        candidate4 = request.form.get('candidate4', '')  # Optional, defaults to empty

        # Call create_election with separate parameters for each candidate
        election_id = create_election(name, date, candidate1, candidate2, candidate3, candidate4)
        
        flash("Election created successfully!", "success")
        return redirect(url_for('admin_dashboard'))  # Redirect to reload the dashboard

    # Render the admin dashboard page on a GET request
    return render_template('admin_dashboard.html', admin_name=session['admin_name'])


#view election for admin 
@app.route('/view_elections')
def view_elections():
    if 'admin_name' in session:
        elections = get_current_elections()  # Fetch current elections with candidates
        return render_template('view_elections.html', elections=elections)
    else:
        flash("You need to log in as admin first.", "error")
        return redirect(url_for('login.html'))
    

#Auditor view of elections
@app.route('/view_electionsAu')
def view_elections_auditor():
    elections = get_current_elections()  # Fetch current elections from the database
    return render_template('view_electionsAu.html', elections=elections)  # Render the view elections page

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
    # Fetch elections from the database (using your get_current_elections function)
    elections = get_current_elections()

    # Find the specific election by ID (you can filter or loop through elections)
    election = next((e for e in elections if e['id'] == election_id), None)

    if not election:
        flash("Election not found.", "error")
        return redirect(url_for('view_elections_voter'))

    if request.method == 'POST':
        # Handle the vote submission
        selected_candidate = request.form['candidate']
        # You can call a function to submit the vote here, like submit_vote_to_db
        #submit_vote_to_db(election_id, selected_candidate)  # Assuming this function exists
        voter_id = session.get('voter_id')
        if voter_id:
            # Get the voter's details from the database (replace this with actual DB query)
            voter_details = get_voter_by_id(voter_id)  # Implement this function to get the voter details
            if voter_details:
                ssn, driver_id, zipcode, voter_account, private_key = voter_details
                contract_address = "0x1234567890abcdef1234567890abcdef12345678"  # Replace with your actual contract address
                contract_abi = contract_abi

                # Create an instance of the Voter class
                voter = Voter(ssn, driver_id, zipcode, voter_account, private_key, contract_address, contract_abi, provider_url)
                # Cast the vote using the Voter class method
                voter.cast_vote(selected_candidate)  # This will send the vote to the blockchain
                
                flash('Vote submitted successfully!', 'success')
                return redirect(url_for('view_elections_voter'))
            else:
                flash("Voter not found.", "error")
                return redirect(url_for('login'))
        else:
            flash("Please log in to vote.", "error")
            return redirect(url_for('login'))

        #flash('Vote submitted successfully!', 'success')
        #return redirect(url_for('view_elections_voter'))
    # If it's a GET request, render the election and candidates
    candidates = [election['candidate1'], election['candidate2'], election['candidate3'], election['candidate4']]
    candidates = [candidate for candidate in candidates if candidate]  # Filter out empty candidates

    return render_template('cast.html', election_title=election['name'], candidates=candidates, election_id=election_id)

def get_candidate_id(selected_candidate):
    # Mapping candidate names to their respective IDs
    candidates = {
        "Alice": 1,
        "Bob": 2
    }
    return candidates.get(selected_candidate, None)

#send vote to blockchain route
@app.route('/submit_vote/<int:election_id>', methods=['POST'])
def submit_vote(election_id):
    selected_candidate = request.form['candidate']
    
    # Call the smart contract to cast the vote on the blockchain
    try:
        # Assuming you have a web3 instance set up
        web3 = Web3(Web3.HTTPProvider('http://localhost:7545'))  # Replace with your provider
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Get the candidate ID (this would depend on how the candidates are stored in your contract)
        candidate_id = get_candidate_id(selected_candidate)  # Implement this mapping
        
        # Send the vote to the blockchain
        transaction = contract.functions.vote(candidate_id).buildTransaction({
            'from': web3.eth.accounts[0],  # The voter's account
            'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0]),
            'gas': 2000000,
            'gasPrice': Web3.toWei('50', 'gwei')
        })
        
        # Sign the transaction
        signed_txn = web3.eth.account.signTransaction(transaction, private_key)  # Ensure private key is set
        
        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        
        return f"Vote cast successfully! Transaction hash: {tx_hash.hex()}"
    
    except Exception as e:
        return f"Error while casting vote: {str(e)}"

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

