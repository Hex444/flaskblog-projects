from flask import Flask, render_template, url_for,flash,redirect, request, abort
from flaskblog.forms import registrationform, Loginform, UpdateAccountform, PostForm
from flaskblog.models import User,Post
from flaskblog import app, db, bcrypt
import secrets
from flask_login import login_user,logout_user, current_user,login_required
import os
from PIL import Image

# posts = [
#     {
#         "author": "max tennyson",
#         "title": "blog post 1",
#         "content": "blueprints of the omnitrix spread through the entire universe, the entire multiverse at danger",
#         "date_posted": "2 Feb, 2022"
#     },
#     {
#         "author": "Sherlock, a great thought to be dead detective",
#         "title": "blog post 2",
#         "content": "Rohit Ghosh caught to be stealing doughnuts from dunkin doughnuts, fined for $2000",
#         "date_posted": "3 Feb, 2022"
#     }
# ]

@app.route("/")
def hello_world():
    posts = Post.query.all()
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route('/account', methods=['POST','GET'])
@login_required
def account():
    form = UpdateAccountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
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

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created!', 'success')
        return redirect(url_for('hello_world'))
    return render_template('create_post.html', title="New Post", form=form, legend="New Post")

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="Update Post", form=form, legend="Update Post")