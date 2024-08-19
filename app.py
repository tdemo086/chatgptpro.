from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from google_sheets import save_user_data, get_user_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/work')
def work():
    if 'username' in session:
        return render_template('work.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user_info = get_user_data(username)
        if user_info:
            return render_template('profile.html', user_info=user_info)
        else:
            return "User not found", 404
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Basic check
        user_info = get_user_data(username)
        if user_info and password == 'expected_password':  # Replace with secure check
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid login", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        payment_method = request.form['payment_method']
        
        # Save to Google Sheets
        save_user_data(username, email, mobile, payment_method)
        
        session['username'] = username
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/task/<task_id>', methods=['POST'])
def complete_task(task_id):
    if 'username' in session:
        # Logic to handle task completion and points
        return jsonify({'success': True})
    return jsonify({'success': False}), 403

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

if __name__ == '__main__':
    app.run(debug=True)




