from flask import Flask, render_template, redirect, url_for, session, flash
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Firebase setup
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')

@app.route('/login')
def login():
    # Redirect to Google Sign-In page using Firebase Authentication
    return redirect(url_for('signin'))

@app.route('/callback')
def callback():
    # This route will handle the callback from Google's OAuth process
    id_token = request.args.get('id_token')
    try:
        # Verify the token with Firebase
        decoded_token = auth.verify_id_token(id_token)
        session['user'] = decoded_token
        flash('Signin successful!', 'success')
        return redirect(url_for('profile'))
    except:
        flash('Authentication failed!', 'danger')
        return redirect(url_for('signin'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('signin'))
    user_data = session['user']
    return render_template('profile.html', user=user_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
    
