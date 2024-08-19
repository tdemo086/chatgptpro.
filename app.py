from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email
import firebase_admin
from firebase_admin import credentials, firestore
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Firebase setup
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Forms
class SignupForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile Number', validators=[DataRequired()])
    whatsapp = StringField('WhatsApp Number', validators=[DataRequired()])
    bkash = StringField('Bkash/Nagad Number', validators=[DataRequired()])
    facebook = StringField('Facebook ID', validators=[DataRequired()])
    dob = StringField('Date of Birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')
    submit = SubmitField('Signup')

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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'email': form.email.data,
            'mobile': form.mobile.data,
            'whatsapp': form.whatsapp.data,
            'bkash': form.bkash.data,
            'facebook': form.facebook.data,
            'dob': form.dob.data,
            'password': form.password.data  # Ensure to hash this in production
        }

        # Save profile picture
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            picture_path = os.path.join('static/images', filename)
            form.profile_picture.data.save(picture_path)
            user_data['profile_picture'] = filename

        # Save to Firebase
        db.collection('users').add(user_data)
        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user_ref = db.collection('users').where('email', '==', form.email.data).get()
        if user_ref:
            user_data = user_ref[0].to_dict()
            if user_data['password'] == form.password.data:
                session['user'] = user_data
                flash('Signin successful!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Invalid credentials', 'danger')
        else:
            flash('User not found', 'danger')

    return render_template('signin.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
