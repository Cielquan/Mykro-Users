# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'test_config.py' created 2020-02-23
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
    tests.test_config
    ~~~~~~~~~~~~~~~~~

    test configs

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import os

import pytest

from app import create_app
from app.config import ProdConfig, get_env_var


def test_get_env_var(monkeypatch):
    """Test get_env_var function"""
    monkeypatch.delenv("TEST_VAR", raising=False)

    #: Test with FLASK_CONFIG unset
    monkeypatch.delenv("FLASK_CONFIG", raising=False)
    with pytest.raises(KeyError):
        assert get_env_var("TEST_VAR")
        assert get_env_var("TEST_VAR", raise_no_default=True)
    with pytest.warns(UserWarning):
        assert get_env_var("TEST_VAR", raise_no_default=False) is None

    #: Test with FLASK_CONFIG set to Prod
    monkeypatch.setenv("FLASK_CONFIG", "Prod")
    with pytest.raises(KeyError):
        assert get_env_var("TEST_VAR")
    with pytest.warns(UserWarning):
        assert get_env_var("TEST_VAR", raise_no_default=False) is None

    #: Test with FLASK_CONFIG set to Dev
    monkeypatch.setenv("FLASK_CONFIG", "Dev")
    with pytest.warns(UserWarning):
        assert get_env_var("TEST_VAR") is None
        assert get_env_var("TEST_VAR", raise_no_default=False) is None

    #: Test with TEST_VAR unset
    with pytest.warns(UserWarning):
        assert get_env_var("TEST_VAR", rv_type=float) is None
    assert get_env_var("TEST_VAR", 2.0, rv_type=float) == 2.0
    assert get_env_var("TEST_VAR", "2", rv_type=float) == 2.0

    #: Test with TEST_VAR set
    monkeypatch.setenv("TEST_VAR", "1.0")
    assert get_env_var("TEST_VAR") == "1.0"
    assert get_env_var("TEST_VAR", rv_type=float) == 1.0
    assert get_env_var("TEST_VAR", 2.0, rv_type=float) == 1.0
    assert get_env_var("TEST_VAR", "2", rv_type=float) == 1.0


def test_development_config(monkeypatch):
    """Test dev config"""
    monkeypatch.setenv("FLASK_CONFIG", "Dev")
    app = create_app()

    assert app.config["SECRET_KEY"]
    assert app.config["JWT_SECRET_KEY"]
    assert app.config["SECRET_KEY"] == app.config["JWT_SECRET_KEY"]
    assert not app.config["TESTING"]
    assert app.config["DEBUG"]
    assert app.config["SQLALCHEMY_DATABASE_URI"]
    assert app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert app.config["REFRESH_TOKEN_EXPIRATION"] == 86400 * 14


def test_testing_config(monkeypatch):
    """Test testing config"""
    monkeypatch.setenv("FLASK_CONFIG", "Test")
    app = create_app()

    assert app.config["SECRET_KEY"]
    assert app.config["JWT_SECRET_KEY"]
    assert app.config["SECRET_KEY"] == app.config["JWT_SECRET_KEY"]
    assert app.config["TESTING"]
    assert not app.config["PRESERVE_CONTEXT_ON_EXCEPTION"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"
    assert app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert app.config["ACCESS_TOKEN_EXPIRATION"] == 3
    assert app.config["REFRESH_TOKEN_EXPIRATION"] == 3


def test_production_config(monkeypatch):
    """Test prod config"""
    monkeypatch.setenv("SECRET_KEY", "TestKey")
    monkeypatch.setenv("JWT_SECRET_KEY", "TestKey_JWT")
    monkeypatch.setenv("FLASK_CONFIG", "Prod")

    monkeypatch.setattr(ProdConfig, "SECRET_KEY", "TestKey")
    monkeypatch.setattr(ProdConfig, "JWT_SECRET_KEY", "TestKey_JWT")

    app = create_app()

    assert app.config["SECRET_KEY"] == os.environ["SECRET_KEY"]
    assert app.config["JWT_SECRET_KEY"] == os.environ["JWT_SECRET_KEY"]
    assert app.config["SECRET_KEY"] != app.config["JWT_SECRET_KEY"]
    assert not app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"]
    assert app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert app.config["REFRESH_TOKEN_EXPIRATION"] == 86400 * 14
