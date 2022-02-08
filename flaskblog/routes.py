from flask import Flask, render_template, url_for,flash,redirect
from flaskblog.forms import registrationform, Loginform
from flaskblog.models import User,Post
from flaskblog import app

posts = [
    {
        "author": "max tennyson",
        "title": "blog post 1",
        "content": "blueprints of the omnitrix spread through the entire universe, the entire multiverse at danger",
        "date_posted": "2 Feb, 2022"
    },
    {
        "author": "Sherlock, a great thought to be dead detective",
        "title": "blog post 2",
        "content": "Rohit Ghosh caught to be stealing doughnuts from dunkin doughnuts, fined for $2000",
        "date_posted": "3 Feb, 2022"
    }
]

@app.route("/")
@app.route("/home")
def hello_world():
    return render_template("home.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registrationform()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', "success")
        return redirect(url_for('hello_world'))
    return render_template("register.html", title='register', form=form)

@app.route("/login", methods=['POST','GET'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == 'password':
            flash('you have been logged in', "success")
            return redirect(url_for('hello_world'))
        else:
            flash("unsuccesful login pls check username and password", "danger")

    return render_template("login.html", title='login', form=form)