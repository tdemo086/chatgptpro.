from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

USERS_FILE = 'users.json'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'adminpass'  # Change this to a secure password

# Helper function to load and save users
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

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
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Invalid credentials'
    return render_template('login.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            return 'Username already exists'
        users[username] = password
        save_users(users)
        return redirect(url_for('login'))
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
    users = load_users()
    return render_template('admin_panel.html', users=users)

# Add a user (admin functionality)
@app.route('/admin/add_user', methods=['POST'])
def add_user():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    username = request.form['username']
    password = request.form['password']
    users = load_users()
    if username in users:
        return 'Username already exists'
    users[username] = password
    save_users(users)
    return redirect(url_for('admin_panel'))

# Delete a user (admin functionality)
@app.route('/admin/delete_user/<username>')
def delete_user(username):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
    return redirect(url_for('admin_panel'))

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
    
