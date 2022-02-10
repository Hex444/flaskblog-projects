from flask import Flask, render_template, url_for,flash,redirect, request
from flaskblog.forms import registrationform, Loginform, UpdateAccountform
from flaskblog.models import User,Post
from flaskblog import app, db, bcrypt
from flask_login import login_user,logout_user, current_user,login_required

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
def hello_world():
    return render_template("home.html", all_posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = registrationform()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', "success")
        return redirect(url_for('login'))
    return render_template("register.html", title='register', form=form)

@app.route("/login", methods=['POST','GET'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('hello_world'))
        else:
            flash("unsuccesful login pls check email and password", "danger")

    return render_template("login.html", title='login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello_world'))

@app.route('/account', methods=['POST','GET'])
@login_required
def account():
    form = UpdateAccountform()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your acc has been updated', category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="account", image_file=image_file, form=form)
