from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, auth, db
import pyrebase

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Firebase Admin SDK initialization
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com/'
})

# Pyrebase initialization
firebase_config = {
    "apiKey": "your-api-key",
    "authDomain": "your-auth-domain",
    "databaseURL": "your-database-url",
    "projectId": "your-project-id",
    "storageBucket": "your-storage-bucket",
    "messagingSenderId": "your-messaging-sender-id",
    "appId": "your-app-id",
    "measurementId": "your-measurement-id"
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']
            db.child("users").child(user_id).set({"name": name, "email": email})
            session['user'] = user
            return redirect(url_for('home'))
        except:
            return "Registration Failed"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect(url_for('home'))
        except:
            return "Login Failed"
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' in session:
        user = session['user']
        user_info = db.child("users").child(user['localId']).get().val()
        return render_template('home.html', user=user_info)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
