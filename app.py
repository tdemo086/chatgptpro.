from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    bkash_number = db.Column(db.String(20), nullable=True)
    nagad_number = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

# Create database tables
with app.app_context():
    db.create_all()

# Define the registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    bkash_number = StringField('Bkash Number', validators=[DataRequired()])
    nagad_number = StringField('Nagad Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user instance
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            mobile_number=form.mobile_number.data,
            bkash_number=form.bkash_number.data,
            nagad_number=form.nagad_number.data,
            password=form.password.data
        )
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Login route (you can expand this with actual login logic)
@app.route('/login', methods=['GET', 'POST'])
def login():
    return "Login Page (To be implemented)"

# Home route (or any other page)
@app.route('/')
def home():
    return "Home Page (To be implemented)"

if __name__ == '__main__':
    app.run(debug=True)




