from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyBFu8Ml90MwZNRNiOjDhWZB5HeKQoVsz3M",
    "authDomain": "dhet-7fc2c.firebaseapp.com",
    "databaseURL": "https://dhet-7fc2c-default-rtdb.firebaseio.com/",
    "projectId": "dhet-7fc2c",
    "storageBucket": "dhet-7fc2c.appspot.com",
    "messagingSenderId": "972635237801",
    "appId": "1:972635237801:web:d6e716d6a0de67ea82a8b8",
    "measurementId": "G-ZXQSWDSEPT"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'adminpass'  # Change this to a secure password

# Home route
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Retrieve user from Firebase Realtime Database
        user_ref = db.child("users").child(username).get()
        if user_ref.val() and user_ref.val().get('password') == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials'
    return render_template('login.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            # Check if the user already exists
            user_ref = db.child("users").child(username).get()
            if user_ref.val():
                return 'Username already exists'
            
            # Save the user to Firebase Realtime Database
            db.child("users").child(username).set({"password": password})
            
            # Log the user in by setting the session
            session['username'] = username
            
            # Redirect to the home page
            return redirect(url_for('home'))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('register.html')

# User logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        return 'Invalid admin credentials'
    return render_template('admin_login.html')

# Admin panel route
@app.route('/admin/panel')
def admin_panel():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    users = db.child("users").get().val()  # Fetch all users from Firebase
    return render_template('admin_panel.html', users=users)

# Add a user (admin functionality)
@app.route('/admin/add_user', methods=['POST'])
def add_user():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    username = request.form['username']
    password = request.form['password']
    
    # Check if the user already exists
    user_ref = db.child("users").child(username).get()
    if user_ref.val():
        return 'Username already exists'
    
    # Save the user to Firebase Realtime Database
    db.child("users").child(username).set({"password": password})
    
    return redirect(url_for('admin_panel'))

# Delete a user (admin functionality)
@app.route('/admin/delete_user/<username>')
def delete_user(username):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    
    # Delete the user from Firebase Realtime Database
    db.child("users").child(username).remove()
    
    return redirect(url_for('admin_panel'))

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
