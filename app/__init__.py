# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file '__init__.py' created 2020-02-22
# is part of the project/program 'Mykro-Users'.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# Github: https://github.com/Cielquan/
# ======================================================================================
"""
    app
    ~~~

    Create app

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import logging
import os

from flask_admin import Admin  # type: ignore
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension  # type: ignore
from flask_migrate import Migrate
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from mykro_common.api_utils import ApiException
from mykro_common.api_utils import ApiFlask as Flask
from werkzeug.utils import find_modules, import_string

from . import config


######################### TDD
db = SQLAlchemy()
migrate = Migrate()

mongo = PyMongo()

cors = CORS()


####################################         REAL
admin = Admin(template_mode="bootstrap3")
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()


def create_app():
    """Factory for creating an application instance"""
    app = Flask(__name__)

    config_name = os.getenv("FLASK_CONFIG", "Prod")
    app.config.from_object(getattr(config, config_name.title() + "Config"))

    # app.app_context().push()

    ######################### TDD
    db.init_app(app)
    migrate.init_app(app, db)

    mongo.init_app(app)

    cors.init_app(app, resources={r"*": {"origins": "*"}})

    ####################################       REAL
    bcrypt.init_app(app)

    toolbar.init_app(app)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

    #: Init flask-admin if Debug = True
    if str(os.getenv("FLASK_DEBUG")) == "True":
        from .admin import UsersAdminView
        from .models import User

        admin = Admin(app, template_mode="bootstrap3")
        admin.add_view(UsersAdminView(User, db.session))

    # register_blueprints(app)
    register_error_handlers(app)

    @app.route("/log")  # TODO 23.02.2020: remove
    def log():
        app.logger.info("test is fucking slow")
        return """<body><div>Hello world</div></body>"""

    @app.route("/")  # TODO 23.02.2020: remove
    def index():
        from mykro_common.api_utils import ApiResult

        return ApiResult(payload={})

    return app


def register_blueprints(app):
    """Find all blueprints and register them"""
    for name in find_modules("app", include_packages=True):
        mod = import_string(name)
        if hasattr(mod, "bp"):
            app.register_blueprint(mod.bp)


def register_error_handlers(app):
    """Register error handlers"""
    app.register_error_handler(ApiException, lambda err: err.to_result())


def init_context(app):
    """Initializing app context"""

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    # from project.users.models import User
    #
    # @app.before_request
    # def before_request():
    #     if hasattr(g, "jwt_claims") and "user_id" in g.jwt_claims:
    #         user = User.query.get(g.jwt_claims["user_id"])
    #         if user is None:
    #             abort(500)
    #         user.ping()
    #         db.session.add(user)
    #         db.session.commit()
