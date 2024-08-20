from flask import Flask, render_template, redirect, url_for, request, session, flash
import firebase_admin
from firebase_admin import credentials, auth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Firebase setup
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Routes
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('home.html')

@app.route('/work')
def work():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('work.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('signin'))
    user_data = session['user']
    return render_template('profile.html', user=user_data)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        token = request.form.get('id_token')
        try:
            decoded_token = auth.verify_id_token(token)
            user_data = {
                'name': decoded_token.get('name'),
                'email': decoded_token.get('email'),
                'user_id': decoded_token.get('uid')
            }
            session['user'] = user_data
            flash('Signin successful!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            flash(f'Error during sign in: {e}', 'danger')
            return redirect(url_for('signin'))
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('signin'))

# Error Handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
    
