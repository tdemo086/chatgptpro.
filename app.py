from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/img'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(100), nullable=True)

class TweetForm(FlaskForm):
    text = StringField('Tweet Text', validators=[DataRequired()])
    image = FileField('Tweet Image')
    submit = SubmitField('Tweet')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = TweetForm()
    if 'username' not in session:
        if request.method == 'POST':
            username = request.form['username']
            if username:
                user = User.query.filter_by(username=username).first()
                if not user:
                    new_user = User(username=username)
                    db.session.add(new_user)
                    db.session.commit()
                session['username'] = username
                return redirect(url_for('home'))
        return render_template('home.html', form=form)

    if form.validate_on_submit():
        text = form.text.data
        image_file = form.image.data
        filename = None
        if image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        tweet = Tweet(username=session['username'], text=text, image=filename)
        db.session.add(tweet)
        db.session.commit()
        flash('New tweet posted!')
        # Notify users with sound logic here (requires JS in frontend)
        return redirect(url_for('home'))

    tweets = Tweet.query.all()
    return render_template('home.html', form=form, tweets=tweets)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_tweet(id):
    tweet = Tweet.query.get_or_404(id)
    form = TweetForm()

    if form.validate_on_submit():
        tweet.text = form.text.data
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            tweet.image = filename
        db.session.commit()
        flash('Tweet updated!')
        return redirect(url_for('home'))

    form.text.data = tweet.text
    return render_template('home.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=9633)

  
