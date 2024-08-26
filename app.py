from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Initialize Firebase Admin SDK
cred = credentials.Certificate('firebase_service_account_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dhet-7fc2c-default-rtdb.firebaseio.com/'
})

# Firebase database reference
users_ref = db.reference('/users')

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
        user = users_ref.child(username).get()
        if user and user['password'] == password:
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
            if users_ref.child(username).get() is not None:
                return 'Username already exists'
            users_ref.child(username).set({'password': password})
            return redirect(url_for('login'))
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
    users = users_ref.get()
    return render_template('admin_panel.html', users=users)

# Add a user (admin functionality)
@app.route('/admin/add_user', methods=['POST'])
def add_user():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    username = request.form['username']
    password = request.form['password']
    if users_ref.child(username).get() is not None:
        return 'Username already exists'
    users_ref.child(username).set({'password': password})
    return redirect(url_for('admin_panel'))

# Delete a user (admin functionality)
@app.route('/admin/delete_user/<username>')
def delete_user(username):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    if users_ref.child(username).get() is not None:
        users_ref.child(username).delete()
    return redirect(url_for('admin_panel'))

# Admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
    
