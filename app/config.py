# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'config.py' created 2020-02-22
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
    app.config
    ~~~~~~~~~~

    Configuration for app.

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import os
import warnings

from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv


APP_BASEDIR = Path(__file__).parents[1]
ENV_FILE = Path(APP_BASEDIR, ".env")

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    print("WARNING: No .env file found.")


EnvVarTypes = Union[str, int, float, bool, None]


def get_env_var(
    var_name: str,
    default: EnvVarTypes = None,
    rv_type: type = str,
    *,
    raise_no_default: Optional[bool] = None,
) -> EnvVarTypes:
    """Func for importing environment variables

    :param var_name: Name of the environment variable.
    :param default: Default value if no value is found for :param var_name:.
    :param rv_type: Type the value of the environment variable should be changed into.
    :param raise_no_default: If an exception should be thrown when no value is found for
                             :param var_name: and :param default: is not set.
                             Defaults to `True` when in production environment and to
                             `False` otherwise.
    """
    if raise_no_default is None:
        raise_no_default = os.getenv("FLASK_CONFIG", "Prod").title() == "Prod"

    msg_no_default = (
        f"Environment variable '{var_name}' not set or empty and no "
        "default value given."
    )
    msg_invalid_bool = (
        f"Environment variable '{var_name}' has an invalid boolean value."
    )

    var = os.getenv(var_name, default)

    if (var == "" or var is None) and default is None:
        if raise_no_default:
            raise KeyError(msg_no_default) from None
        warnings.warn(msg_no_default)
        return None

    if rv_type is bool:
        if str(var).lower() in {"1", "y", "yes", "t", "true"}:
            return True
        if str(var).lower() in {"0", "n", "no", "f", "false"}:
            return False
        raise KeyError(msg_invalid_bool) from None

    return rv_type(var)


class Config:  # pylint: disable=R0903
    """Base configuration"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = get_env_var("SECRET_KEY")
    JWT_SECRET_KEY = get_env_var("JWT_SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = get_env_var("MONGO_DATABASE_URL", "mongodb://mongo:27017/users")
    SQLALCHEMY_DATABASE_URI = os.environ.get(  # TODO 23.02.2020: which DB to use
        "DATABASE_URL", "sqlite:///" + os.path.join(APP_BASEDIR, "users.sqlite")
    )

    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 86400 * 14  # 14 days


class DevConfig(Config):  # pylint: disable=R0903
    """Development configuration"""

    DEBUG = True
    SECRET_KEY = get_env_var(
        "SECRET_KEY", "some-funny-secret-string-would-be-nice-to-brighten-the-devs-mood"
    )
    JWT_SECRET_KEY = get_env_var("JWT_SECRET_KEY", SECRET_KEY)

    BCRYPT_LOG_ROUNDS = 4


class TestConfig(Config):  # pylint: disable=R0903
    """Testing configuration"""

    TESTING = True
    SECRET_KEY = get_env_var(
        "SECRET_KEY", "some-funny-secret-string-would-be-nice-to-brighten-the-devs-mood"
    )
    JWT_SECRET_KEY = get_env_var("JWT_SECRET_KEY", SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # TODO 23.02.2020: how DB use for testing

    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3


class ProdConfig(Config):  # pylint: disable=R0903
    """Production configuration"""
