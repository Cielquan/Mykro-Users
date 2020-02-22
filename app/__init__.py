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
import os

from flask import Flask

from . import config


def app_factory():
    """Factory for creating an application instance"""
    app = Flask(__name__)

    config_name = os.environ.get("FLASK_CONFIG", "Dev")
    app.config.from_object(getattr(config, config_name.title() + "Config"))

    return app


def create_app():
    """Create an app instance and init ints context"""
    return app_factory()
