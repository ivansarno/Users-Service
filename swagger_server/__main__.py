#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server.database import db


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Users'})
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../users.db'
    db.init_app(app.app)
    db.create_all(app=app.app)
    app.run(port=8080)


if __name__ == '__main__':
    main()
