from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import add_voter, get_voter, create_election, get_current_elections  # Import the database functions



app = Flask(__name__)
app.secret_key = 'cis454'  # Set a secret key for session management

# Pre-defined admin ID (for demonstration purposes, use a secure method in production)
ADMIN_ID = 'adminid'  # Replace with your actual admin ID

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
            print(f"Admin ID entered: {user_id}")  # Debugging statement
            if user_id == ADMIN_ID:  # Validate admin ID
                session['admin_name'] = user_id  # Store admin name in session
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
            else:
                flash("Invalid admin ID, please try again.", "error")  # Flash error message
                return redirect(url_for('login'))  # Redirect back to login page

        elif role == 'auditor':
            user_id = request.form['auditor_id']  # Get user ID from form
            session['auditor_name'] = user_id  # Store auditor name in session
            return redirect(url_for('auditor_dashboard'))  # Redirect to auditor dashboard

        elif role == 'voter':
            ssn = request.form['ssn']          # Get SSN from form
            zipcode = request.form['zipcode']  # Get Zipcode from form
            driver_id = request.form['driver_id']  # Get Driver ID from form
            
            # Validate voter credentials
            voter_info = get_voter(ssn)  # Get voter info based on SSN
            if voter_info and voter_info[1] == zipcode and voter_info[2] == driver_id:
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
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_name' in session:
        return render_template('admin_dashboard.html', admin_name=session['admin_name'])
    else:
        flash("You need to log in as admin first.", "error")  # Flash an error if not logged in
        return redirect(url_for('login'))
    
# Create election route
@app.route('/create_election', methods=['GET', 'POST'])
def create_election_view():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        create_election(name, date)  # Save the election to the database
        return redirect(url_for('admin_dashboard'))  # Redirect back to the admin dashboard after creating

    return render_template('create_election.html')  # Render the create election page

# View current elections route
@app.route('/view_elections')
def view_elections():
    elections = get_current_elections()  # Fetch current elections from the database
    return render_template('view_elections.html', elections=elections)  # Render the view elections page

# Auditor dashboard route
@app.route('/auditor_dashboard')
def auditor_dashboard():
    return render_template('auditor_dashboard.html', auditor_name=session.get('auditor_name'))  # Render the auditor dashboard template

# Voter dashboard route
@app.route('/voter_dashboard')
def voter_dashboard():
    return render_template('voter_dashboard.html')  # Render the voter dashboard template

# Signup route for new voters
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        ssn = request.form['ssn']
        zipcode = request.form['zipcode']
        driver_id = request.form['driver_id']
        
        if add_voter(ssn, zipcode, driver_id):
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        else:
            return "Voter with this SSN already exists", 400  # Bad request error

    return render_template('signup.html')  # Render the signup page

# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('index'))  # Redirect to the home page

# Run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

for rule in app.url_map.iter_rules():
    print(rule)