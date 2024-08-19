from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

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
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add login logic here
        session['logged_in'] = True
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Add registration logic here
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


