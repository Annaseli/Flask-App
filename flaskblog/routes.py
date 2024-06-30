import os
import secrets
from PIL import Image
from flask import render_template, url_for, redirect, flash, request, abort
from flaskblog import app, bcrypt, db
from flask_login import login_user, login_required, logout_user, current_user
from flaskblog.forms import RegisterForm, LoginForm, UpdateAccountForm, AddPost, EditPost
from flaskblog.models import User, Post


@app.route("/")
@app.route("/home")
def home():
    paginated_posts = Post.query.paginate(per_page=5)
    while paginated_posts.page != 0:
        posts = []
        for posts_in_page in paginated_posts:
            posts.append(posts_in_page)
        return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # create the user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # add the user to db:
        db.session.add(user)
        db.session.commit()
        flash('Account was created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # search for the user in the db
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)  # login the user
            next_page = request.args.get('next')
            return redirect(url_for(next_page)) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email or password', 'danger')
    return render_template('login.html', title='Login', form=form)


def save_image(form_image):
    # create image path
    _, f_ext = os.path.splitext(form_image.filename)
    random_hex = secrets.token_hex(8)
    image_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', image_name)

    # save the resized image
    img = Image.open(form_image)
    img.thumbnail((125, 125))
    img.save(picture_path)

    return image_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            image_path = save_image(form.image_file.data)
            current_user.image_file = image_path
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account was updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/add_post", methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post was added!', 'success')
        return redirect(url_for('my_posts'))

    return render_template('add_post.html', title='Add Post', form=form)


@app.route("/post/my_posts", methods=['GET', 'POST'])
@login_required
def my_posts():
    # get all the current user's posts
    #my_posts = Post.query.filter_by(user_id=current_user.id)
    my_posts = current_user.posts
    return render_template('my_posts.html', title='My Posts', posts=my_posts)

@app.route("/post/edit_post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # get the post with this id and if it doesn't exist return 404 error
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = EditPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post was updated!', 'success')
        return redirect(url_for('my_posts'))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('add_post.html', title='Edit Post', form=form)

@app.route("/post/delete_post/<int:post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    # get the post with this id and if it doesn't exist return 404 error
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your article has been deleted!', 'success')
    return redirect(url_for('my_posts'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))