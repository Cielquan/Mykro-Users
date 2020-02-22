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

from dotenv import load_dotenv


APP_BASEDIR = Path(__file__).parents[1]
ENV_FILE = Path(APP_BASEDIR, ".env")

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    warnings.warn("No .env file found.")


def get_env_var(var_name, default=None, rv_type_class=str, *, raise_no_default=True):
    """Func for importing environment variables"""
    var = os.environ.get(var_name, default)

    msg_no_default = (
        f"Environment variable '{var_name}' not set or empty and no "
        "default value given."
    )
    msg_invalid_bool = (
        f"Environment variable '{var_name}' has an invalid boolean value."
    )

    if var == "" or var is None:
        if raise_no_default:
            raise KeyError(msg_no_default) from None
        warnings.warn(msg_no_default)
        return None

    if rv_type_class is bool:
        if var.lower() in {"1", "y", "yes", "t", "true"}:
            return True
        if var.lower() in {"0", "n", "no", "f", "false"}:
            return False
        raise KeyError(msg_invalid_bool) from None

    return rv_type_class(var)


class Config:  # pylint: disable=R0903
    """Base configuration"""

    DEBUG = False
    TESTING = False
    SECRET_KEY = get_env_var("SECRET_KEY")


class DevConfig(Config):  # pylint: disable=R0903
    """Development configuration"""

    DEBUG = True
    SECRET_KEY = get_env_var(
        "SECRET_KEY", "some-funny-secret-string-would-be-nice-to-brighten-the-devs-mood"
    )


class TestConfig(Config):  # pylint: disable=R0903
    """Testing configuration"""

    TESTING = True
    SECRET_KEY = get_env_var(
        "SECRET_KEY", "some-funny-secret-string-would-be-nice-to-brighten-the-devs-mood"
    )


class ProdConfig(Config):  # pylint: disable=R0903
    """Production configuration"""