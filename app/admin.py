# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'admin.py' created 2020-02-23
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
    app.admin
    ~~~~~~~~~

    admin interface

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
from flask import current_app
from flask_admin.contrib.sqla import ModelView  # type: ignore

from app import bcrypt


class UsersAdminView(ModelView):
    column_searchable_list = (
        "username",
        "email",
    )
    column_editable_list = (
        "username",
        "email",
        "created_at",
    )
    column_filters = (
        "username",
        "email",
    )
    column_sortable_list = (
        "username",
        "email",
        "active",
        "created_at",
    )
    column_default_sort = ("created_at", True)

    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(
            model.password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()
