from flask import render_template, url_for, flash, redirect

from apc import app
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
