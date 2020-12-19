from flask import Flask, render_template

app = Flask(__name__)

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
def to_rent():
    return render_template('torent.html', title='to Rent')

@app.route('/forsale')
def for_sale():
    return render_template('forsale.html', title='for Sale')


if __name__ == '__main__':
    app.run()
