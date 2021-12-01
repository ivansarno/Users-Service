#!/usr/bin/env python3

import connexion
from sqlalchemy.exc import IntegrityError

from swagger_server import encoder
from swagger_server.database import User as DBUser
from swagger_server.database import db


def _create_admin(app):  # pragma: no cover
    with app.app.app_context():
        try:
            example = DBUser()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'admin@example.com'
            example.date_of_birth = "05/10/2000"
            example.is_admin = True
            example.content_filter = False
            example.set_password('admin')
            example.points = 1000
            db.session.add(example)
            db.session.commit()
        except IntegrityError:
            pass


def main():  # pragma: no cover
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Users'})
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
    db.init_app(app.app)
    db.create_all(app=app.app)
    _create_admin(app)
    app.run(port=8080)


if __name__ == '__main__':  # pragma: no cover
    main()
