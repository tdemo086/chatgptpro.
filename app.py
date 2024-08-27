from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Database model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)

# Create the database
@app.before_first_request
def create_tables():
    db.create_all()

# Route for the homepage
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

# Route to create a new post
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']
        image = request.files['image']

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_post = Post(name=name, text=text, image=filename)
        db.session.add(new_post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)
            
