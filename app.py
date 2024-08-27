from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, db, auth
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Firebase Admin SDK initialization
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dhet-7fc2c.firebaseio.com'
})

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            # Store user details in Firebase Realtime Database
            db.reference(f'users/{user.uid}').set({
                'name': name,
                'email': email,
                'points': 0
            })
            return redirect(url_for('login'))
        except Exception as e:
            return str(e)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            session['user_id'] = user.uid
            return redirect(url_for('home'))
        except Exception as e:
            return str(e)
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.reference(f'users/{user_id}').get()
        return render_template('home.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
            
