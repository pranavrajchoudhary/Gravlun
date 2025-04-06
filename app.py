from flask import Flask, render_template, request, redirect, url_for, session, flash
import os # Good practice for secret key

app = Flask(__name__)

# --- IMPORTANT: Set a Secret Key for Sessions ---
# Sessions are cryptographically signed, so you need a secret key.
# Keep this key secret in a real application (e.g., environment variable).
# For development, you can use os.urandom or a hardcoded string.
app.secret_key = os.urandom(24)  # Generates a random key each time the app starts
# Or use a fixed key for development:
# app.secret_key = 'your_very_secret_key_here_change_me'

# Predefined login credentials
USERNAME = "Astr1137"
PASSWORD = "Vishma@0101"

# --- Routes ---

@app.route('/')
def home_page():
    # If user is already logged in (session exists), go to index
    if 'username' in session:
        return redirect(url_for('index'))
    # Otherwise, show the login page
    return render_template('login.html')

# Renamed login_page route to just /login and handle both GET/POST
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, don't show login page again
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username_attempt = request.form.get('username') # Use .get() to avoid KeyError
        password_attempt = request.form.get('password')

        if username_attempt == USERNAME and password_attempt == PASSWORD:
            # --- Login Successful: Store user in session ---
            session['username'] = username_attempt
            flash('Login Successful!', 'success') # Optional: Provide feedback
            # Redirect to the intended page (index in this case)
            return redirect(url_for('index'))
        else:
            # --- Login Failed ---
            flash('Invalid Credentials. Please try again.', 'danger') # Use flash for errors
            # Re-render login page with error message
            # No need to pass error explicitly if using flash
            return render_template('login.html')

    # --- If request.method is GET, just show the login page ---
    return render_template('login.html')

@app.route('/logout')
def logout():
    # --- Remove user from session ---
    session.pop('username', None) # Safely remove the username
    flash('You have been logged out.', 'info') # Optional: Feedback
    return redirect(url_for('login')) # Redirect to login page

# --- Protected Routes ---
# These routes now require the user to be logged in

@app.route('/index')
def index():
    # --- Check if user is logged in ---
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    # User is logged in, proceed to render the index page
    # You can pass the username to the template if needed
    return render_template('index.html', username=session['username'])

@app.route('/store')
def store():
    # --- Check if user is logged in ---
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    # User is logged in, proceed
    return render_template('store.html')

@app.route('/bin')
def bin():
    # --- Check if user is logged in ---
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    # User is logged in, proceed
    return render_template('bin.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
