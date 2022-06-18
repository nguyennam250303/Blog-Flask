from flaskblog import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flaskblog import login
from flask_login import UserMixin

@login.user_loader
def load_user(id_user):
    return User.query.get(int(id_user))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=60), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=120), nullable=False, unique=True)
    posts = db.relationship("Post", backref="author", lazy=True)

    def set_password(self, typedPasswordByUser):
        self.password_hash = generate_password_hash(typedPasswordByUser)

    def check_password(self, attempted_password):
        return check_password_hash(self.password_hash,attempted_password)



    def __repr__(self):
        return f"author :{self.username}"
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name_post = db.Column(db.String(length=30), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    time_stamp = db.Column(db.DateTime(), default=datetime.utcnow())
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Name post :{self.name_post}"