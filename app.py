from flask import Flask, render_template, request, redirect, url_for, flash, session
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key for production

# Initialize Firebase
cred = credentials.Certificate({
    "type": "service_account",
  "project_id": "dhet-7fc2c",
  "private_key_id": "12d1febe034dc7d29522b711dc763b1f5d2ecb46",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDC62hZxo/25Hni\nUEMixToI1knA0vLj7c62sfShKIr+L8HHI1kuJIhwqbEEWV6RdrxKF1XA6Z7eAjr5\n83AA4klr73wZGR5MRjV4ab9EnC/pWs3vtfuD0KGMOj7HPL38/pJxbHFiYbajPvPZ\n31HPukVLjhY7WYzPb9sUhbF676NW2oHYg+0RpVduyBkDjjBRkwAMprFWiR0kvPRu\nHhQ2mIBmS4NyJVZ118uOUPIezaeE15tE0akW4+ATyLu0h19778/3hewlwwGo+BKc\n4auxOPfhOR3ed+/tyWfJmU1sXj7Go+QaXgzawZpoxcdkw8hlV5d3+M226iQ5/ypG\nKKVHBrepAgMBAAECggEARfcBydfALTrtlRKCRqTMpAdnCdOuY6oknOdbi81ltr+l\nqrlBdZKfdvEyHQGHNGeORnoByfERmVbrnHSJK4gOGrQns0qU2YQKBWLPyOzXNcfm\nS7jiwvnMQu1VQ2bGO12Vaykluc6hJA+gr/+8+fc+kFQ8HqmSJZNc7AzhG+OQmcfL\nZ8uDfyawdOYwKtTVxIGG+RPVQ/SQae16kcNriWiCbXiWhLgKahgpQHWJxGkdXFXc\nfdzijO7xI+trCs2s1Fbc3aikKY2XSig9uJGsgXIs1lrTcuk6L2JX/OEs62AMHtMm\nHkKL3+baZK8Yk3BrOQUQCqFFHgPrKvLZg+8NSKvW0QKBgQD8mqEI3z9kINaDHPe8\nKrVKG66WPlsEcjHJ0GyXCTSnKw2yXr8ZNZtXEB6tP6Bj+PsdHBy2M9sLPlulyTmf\nmN2njSjmWsIwHQ4XL7VBwr44IulESyecHnV36KsUc2FiJvpb7VgC3nfqYH9vB+/q\nS3/oM87Mw5oGB7QGgIqA7Ry4twKBgQDFij/sOI5DcpxXmSMMlE7k+Ai1dEUIY91C\nN65MEQIJ1TfEIhWstUKkt6tNQHqCpilx4vTu8wmMf8vnwM+EOpz2Q2M6RCvylqvH\ncVvksh4ixLboysN+8QOsrT9uEr86kt9TJBe7hIz1xb6l/hhxITIsBtDmiRalPSdw\nqMBMwAXynwKBgFy1j8bG0Og52SET36SS9Ch30nLX/eW616UfNsuUGFwGRCej+HUT\nJKkmhGvHf2FRvzAm4i7JB2qv/0jwepKlsyxMdaddxgmMkGBYJSk2hUPrJDvpbWcy\nEqDopumBk0tHzPkyOewLpG1D72Fbw2T1QsOBSDQE0iHGb/827B53Z+QvAoGBAKDg\nJ5D8ujeJ1nOsvpOXEO1+ZrFIYJQlqGMuL5+5VjylzcXIsHg4Im89OaAve9Z89lHO\nsQUNH2CyD2DNcPNSPNR+Kwifzl7BgGJsGpeUy+Aq7n+F6lKue/ycF4VQdTaBuKjg\nQwevOpFKGyraVhOEInUik+y8BppJxJ4GgJ3A4NcnAoGAdS7ELbZkxqHFNEFYI1er\nZd1qB0tn26I9Nnr+Tw4qv4h743khT1bh6tFcJqH6opweff9REfl1EX3KuKWykeRA\nS9AvDTPw1s5eJdl7H6oQ86sE3rOKQ0/TjpsmECgZkcv6xwqvgdBAioBlAv/1/KNV\nXZe7sfgcbxK2b0PJQBHJ1Jw=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-a5sbs@dhet-7fc2c.iam.gserviceaccount.com",
  "client_id": "100644738377023967334",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-a5sbs%40dhet-7fc2c.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)

# Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            print(f"User created: {user.uid}")
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")
            flash(f'Error: {str(e)}', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            # Note: Firebase Auth doesn't support password verification directly, 
            # so this example assumes you are using Firebase's client SDKs for this.
            # Here, you might use a custom approach or the client SDK for password validation.
            # If successful, set session data.
            session['user'] = user.uid
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(f"Error: {e}")
            flash(f'Error: {str(e)}', 'danger')
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
