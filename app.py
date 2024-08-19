from flask import Flask, render_template, redirect, url_for, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulate a user store
users = {}
points = {}
referral_links = {}

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
        user_info = users.get(username, {})
        user_points = points.get(username, 0)
        refer_link = referral_links.get(username, '')
        return render_template('profile.html', user_info=user_info, points=user_points, refer_link=refer_link)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Password validation is omitted for simplicity
        if username in users:
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
        
        # Save user info
        users[username] = {'email': email, 'password': password, 'mobile': mobile, 'payment_method': payment_method}
        points[username] = 0
        referral_links[username] = f"http://yourwebsite.com/referral/{username}"
        
        session['username'] = username
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/task/<task_id>', methods=['POST'])
def complete_task(task_id):
    if 'username' in session:
        username = session['username']
        if username not in points:
            points[username] = 0
        points[username] += 50  # Add 50 points for completing a task
        return jsonify({'success': True, 'points': points[username]})
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

@app.route('/level')
def level():
    return render_template('level.html')

if __name__ == '__main__':
    app.run(debug=True)



