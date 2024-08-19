from flask import Flask, render_template, redirect, url_for, request, session
import firebase_admin
from firebase_admin import credentials, db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Initialize Firebase Admin SDK
cred = credentials.Certificate("static\serviceAccountKey..json")  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tdemo-d2f6e-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/work')
def work():
    if 'logged_in' in session:
        return render_template('work.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'logged_in' in session:
        user = session['user']
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Firebase Realtime Database logic to authenticate user
        ref = db.reference('users')
        users = ref.get()

        for user_key, user_data in users.items():
            if user_data['email'] == email and check_password_hash(user_data['password'], password):
                session['logged_in'] = True
                session['user'] = user_data
                return redirect(url_for('home'))

        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        mobile_number = request.form['mobile_number']
        bkash_nagad_number = request.form['bkash_nagad_number']

        # Firebase Realtime Database logic to save user data
        ref = db.reference('users')
        ref.push({
            'username': username,
            'email': email,
            'password': password,
            'mobile_number': mobile_number,
            'bkash_nagad_number': bkash_nagad_number,
            'points': 0
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/level')
def level():
    return render_template('level.html')

if __name__ == '__main__':
    app.run(debug=True)

