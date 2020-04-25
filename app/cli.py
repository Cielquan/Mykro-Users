# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'cli.py' created 2020-02-23
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
    app.cli
    ~~~~~~~

    CLI of the app

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""


def register(app):
    """Register CLI commands"""
    from app import db
    from app.models import User

    # @app.cli.group()
    # def translate():
    #     """Translation and localization commands."""
    #     pass
    #
    # @translate.command()
    # @click.argument("lang")
    # def init(lang):
    #     """Initialize a new language."""
    #     if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
    #         raise RuntimeError("extract command failed")
    #     if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
    #         raise RuntimeError("init command failed")
    #     os.remove("messages.pot")
    #
    # @translate.command()
    # def update():
    #     """Update all languages."""
    #     if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
    #         raise RuntimeError("extract command failed")
    #     if os.system("pybabel update -i messages.pot -d app/translations"):
    #         raise RuntimeError("update command failed")
    #     os.remove("messages.pot")
    #
    # @translate.command()
    # def compile():
    #     """Compile all languages."""
    #     if os.system("pybabel compile -d app/translations"):
    #         raise RuntimeError("compile command failed")

    @app.command("recreate_db")
    def recreate_db():
        db.drop_all()
        db.create_all()
        db.session.commit()

    @app.command("seed_db")
    def seed_db():
        db.session.add(
            User.add_user(
                {
                    "username": "michael",
                    "email": "hermanmu@gmail.com",
                    "password": "supersecret",
                }
            )
        )
        db.session.add(
            User.add_user(
                {
                    "username": "michaelherman",
                    "email": "michael@mherman.org",
                    "password": "supersecret",
                }
            )
        )
        db.session.commit()
