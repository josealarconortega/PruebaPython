import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "prueba.db"))
ma = Marshmallow()


def db_init(app):
    db.init_app(app)

    ma.init_app(app)
    db.create_all()
