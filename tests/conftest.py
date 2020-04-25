# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'conftest.py' created 2020-02-23
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
    tests.conftest
    ~~~~~~~~~~~~~~

    Test fixtures

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import os

import pytest

from mykro_common.test import client, client_class, token_admin, token_roleless

from app import create_app, db
from app.models import User


@pytest.yield_fixture(scope="session", autouse=True)
def app():
    """Pytest fixture yielding an app testing instance"""
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    os.environ["FLASK_DEBUG"] = "False"
    FLASK_CONFIG = os.getenv("FLASK_CONFIG")
    os.environ["FLASK_CONFIG"] = "Test"

    app = create_app()
    with app.app_context():
        yield app

    os.environ["FLASK_DEBUG"] = FLASK_DEBUG
    os.environ["FLASK_CONFIG"] = FLASK_CONFIG


@pytest.yield_fixture(scope="class")
def test_db():
    """Pytest fixture yielding an db testing instance"""
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="session")
def add_user():
    """Pytest fixture returning the User model's add_user function"""
    return User.add_user
