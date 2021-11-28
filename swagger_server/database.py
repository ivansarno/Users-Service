import json

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False, unique=True)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    date_of_birth = db.Column(db.Unicode(128))
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

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def add_points(self, points):
        self.points = self.points + points

    def set_points(self, points):
        self.points = points

    def get_points(self):
        return self.points

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                self.set_password(value)
            # prevent privilege de/escalation
            elif key != 'is_admin' or key != 'is_anonymous' or key != 'points':
                setattr(self, key, value)

    def get_content_filter_status(self):
        return self.content_filter

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_email = db.Column(db.Unicode(128), nullable=False)
    reported_email = db.Column(db.Unicode(128), nullable=False)
    description = db.Column(db.Unicode(1024), nullable=False)
    timestamp = db.Column(db.Unicode(128), nullable=False)

    def __init__(self, *args, **kw):
        super(Report, self).__init__(*args, **kw)

    def add_report(self, author_email, reported_email, description, timestamp):
        self.author_email = author_email
        self.reported_email = reported_email
        self.description = description
        self.timestamp = timestamp

    def get_id(self):
        return self.id

