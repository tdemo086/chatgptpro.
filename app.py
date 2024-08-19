from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mining')
def mining():
    return render_template('mining.html')

@app.route('/collection')
def collection():
    return render_template('collection.html')

@app.route('/marketplace')
def marketplace():
    return render_template('marketplace.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
