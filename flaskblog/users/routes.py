from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (Registrationform, Loginform, UpdateAccountform,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users=Blueprint('users', __name__)

emojis={
    "smile":"😁",
    "upside-down-smile":"🙃",
    "tools":"🛠"
}

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = Registrationform()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', "success")
        return redirect(url_for('users.login'))
    return render_template("register.html", title='register', form=form)

@users.route("/login", methods=['POST','GET'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("unsuccesful login pls check email and password", "danger")

    return render_template("login.html", title='login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['POST','GET'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template("user_posts.html", posts=posts, user=user,emojis=emojis)

@users.route('/reset_password', methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('an email has been sent with instructions to reset your password link expires in 15 mins', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)



@users.route('/reset_password/<token>', methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired Token', 'warn')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_pw
        db.session.commit()
        flash(f'Password Updated {emojis.get("upside-down-smile")}!', "success")
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



# smtp acess is blocked in server service providers lol