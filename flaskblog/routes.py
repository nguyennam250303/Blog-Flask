from flaskblog import app, db
from flask import render_template, request, redirect, flash, url_for
from flaskblog.forms import LoginForm, RegisterForm, ViewPost, CreatePostForm
from flaskblog.models import Post, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home_page.html")



@app.route("/posts", methods = ["GET","POST"])
@login_required
def posts_page():
    posts = Post.query.all()
    viewpost = ViewPost()
    if request.method == "POST":
        id_post_current = request.form.get("detailed-view")
        body = Post.query.filter_by(id=id_post_current).first().body
        return render_template("body_post.html",posts=posts,body=body)
    return render_template("posts.html", posts=posts, viewpost=viewpost)




@app.route("/login", methods =["GET","POST"])
def login_page():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        attempted_user = User.query.filter_by(username = form_login.username.data).first()
        if attempted_user and attempted_user.check_password(form_login.password.data):
            login_user(attempted_user)
            flash(f"You have logged in Successfully on username :{form_login.username.data}", category="success")
            return redirect(url_for("posts_page"))
        else:
            flash("Username or password Invalid", category="danger")
    return render_template("login.html", form_login=form_login)
@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have logged out successfully", category="success")
    return redirect(url_for("login_page"))

@app.route("/user/<username>",methods = ["GET", "POST"])
@login_required
def info_user_page(username):

    user = User.query.filter_by(username=username).first_or_404()
    post = user.posts
    viewpost = ViewPost()
    if request.method == "POST":
        id_post_current = request.form.get("detailed-view")
        body = Post.query.filter_by(id=id_post_current).first().body
        return render_template("body_post_user.html", post=post, body=body, username=username)
    return render_template("info_user_page.html",user=user, post=post,viewpost=viewpost)

@app.route("/register", methods =["GET","POST"])
def register_page():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        user_created = User(username=form_register.username.data,
                            email_address=form_register.email_address.data)

        user_created.set_password(form_register.password1.data)
        db.session.add(user_created)
        db.session.commit()
        login_user(user_created)
        flash("You have created account successfully",category="success")
        return redirect(url_for("posts_page"))

    if form_register.errors:
        for error in form_register.errors.values():
            flash(f"There was a error in creating account process :{error[0]}",category="danger")


    return render_template("register.html", form_register=form_register)


@app.route("/create_post", methods=["GET","POST"])
@login_required
def create_post_page():
    create_post_form = CreatePostForm()

    if request.method == "POST":
        created_post = Post(name_post=create_post_form.name_post.data
                            , body=create_post_form.body.data)
        created_post.user_id = current_user.id
        db.session.add(created_post)
        db.session.commit()
        
        flash(f"You have just created a post with name '{create_post_form.name_post.data}' successfully", category="success")
        return redirect(url_for("posts_page"))

    return render_template("create_post.html",create_post_form=create_post_form)
