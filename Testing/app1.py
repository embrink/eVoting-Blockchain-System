from flask import Flask, render_template, request, redirect, url_for, session, flash

app1 = Flask(__name__)
app1.secret_key = 'secret_key'  # Set a secret key for session management

# Home route
@app1.route('/')
def index():
    print("Index route accessed")
    return render_template('login.html')  # Render the login page template

# Login route
@app1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("Login POST request received")
        role = request.form['role']  # Get user role from form
        print(f"Role selected: {role}")

        if role == 'admin':
            user_id = request.form['user_id']  # Get admin ID from form
            if user_id == 'adminid':  # Pre-defined admin ID for demonstration
                session['user_role'] = 'admin'
                return redirect(url_for('dashboard'))  # Redirect to dashboard
            else:
                flash("Invalid admin ID, please try again.", "error")
                return redirect(url_for('login'))

        elif role == 'voter':
            ssn = request.form['ssn']  # Get SSN from form
            # Assume SSN validation logic here
            session['user_role'] = 'voter'
            return redirect(url_for('dashboard'))  # Redirect to dashboard

        elif role == 'auditor':
            user_id = request.form['user_id']  # Get auditor ID from form
            session['user_role'] = 'auditor'
            return redirect(url_for('dashboard'))  # Redirect to dashboard

        else:
            flash("Invalid role selected", "error")
            return redirect(url_for('login'))

    return render_template('login.html')  # Render the login page template

# Dashboard route
@app1.route('/dashboard')
def dashboard():
    role = session.get('user_role', None)
    if role:
        return render_template('dashboard.html', role=role)
    else:
        flash("You need to log in first.", "error")
        return redirect(url_for('login'))

# Logout route
@app1.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('index'))  # Redirect to the home page

# Run app in debug mode
if __name__ == '__main__':
    app1.run(debug=True)
