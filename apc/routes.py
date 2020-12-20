from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from apc import app, db, bcrypt
from apc.forms import SignupForm, LoginForm
from apc.models import User, Post


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created.  You are now able to log in.', category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Log in unsuccessful. Please check email and password', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
