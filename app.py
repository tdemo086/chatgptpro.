from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
import firebase_admin
from firebase_admin import credentials, auth
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Firebase setup
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Forms
class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signin')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/work')
def work():
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
        # Get the Google token from the request (after Google sign-in)
        token = request.form.get('id_token')

        try:
            # Verify the token with Firebase
            decoded_token = auth.verify_id_token(token)
            user_data = decoded_token

            # Save user session
            session['user'] = user_data
            flash('Signin successful!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            flash(f'Error verifying token: {e}', 'danger')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
    
