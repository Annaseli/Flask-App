from flask import Flask, render_template, url_for, redirect, flash
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f9ac5193def46b21bcbf5ed7cd295aef'

posts = [
    {
        "author": "AS",
        "date_posted": "25/06/24",
        "title": 'A',
        "content": "abc"
    },
    {
        "author": "BC",
        "date_posted": "25/06/24",
        "title": 'B',
        "content": "dvggrgi"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful.', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)