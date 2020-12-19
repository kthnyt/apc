import os
from datetime import datetime

from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from forms import SignupForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), default='default.jpg', nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='agent', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'agent': 'Amanda Tsitsi',
        'title': '3 Bedroom House, North End, Bulawayo, Zimbabwe',
        'content': 'First property listing',
        'date+posted': 'December 19, 2020'
    },
    {
        'agent': 'Buhle Faith',
        'title': '2 Bedroom Apartment, Mkhosana, Victoria Falls, Zimbabwe',
        'content': 'Second property listing',
        'date+posted': 'December 19, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/torent')
def torent():
    return render_template('torent.html', title='to Rent')


@app.route('/forsale')
def forsale():
    return render_template('forsale.html', title='for Sale')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('home'))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@apc.com' and form.password.data == 'password':
            flash(f'Welcome {form.email.data.split("@")[0].capitalize()}. You have been logged !', category='success')
            return redirect(url_for('home'))
        else:
            flash(f'Log in unsuccessful. Please check username and password', category='danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run()
