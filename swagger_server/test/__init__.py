import logging
import os

import connexion
from flask_testing import TestCase

from swagger_server.database import db
from swagger_server.encoder import JSONEncoder


class BaseTestCase(TestCase):

    def create_app(self):
        self._cleanup()
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./T_users.db'
        db.init_app(app.app)
        db.create_all(app=app.app)

        return app.app

    def _cleanup(self):
        if os.path.exists('./T_users.db'):
            os.remove('./T_users.db')
