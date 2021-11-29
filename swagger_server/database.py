from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    firstname = db.Column(db.Unicode(128), nullable=False)
    lastname = db.Column(db.Unicode(128), nullable=False)
    password = db.Column(db.Unicode(128), nullable=False)
    date_of_birth = db.Column(db.Unicode(128), nullable=False)
    points = db.Column(db.Integer, default=0)
    content_filter = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_email = db.Column(db.Unicode(128), nullable=False)
    reported_email = db.Column(db.Unicode(128), nullable=False)
    description = db.Column(db.Unicode(1024), nullable=False)
    timestamp = db.Column(db.Unicode(128), nullable=False)

    def __init__(self, *args, **kw):
        super(Report, self).__init__(*args, **kw)
