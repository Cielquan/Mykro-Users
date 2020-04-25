# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'test_admin.py' created 2020-02-23
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
    tests.test_admin
    ~~~~~~~~~~~~~~~~

    test admin interface

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import os

from app import create_app, db


# from mykro_common.test import RequestMethods


def test_admin_view_on(monkeypatch):
    """Test admin interface on"""
    monkeypatch.setenv("FLASK_CONFIG", "Test")
    monkeypatch.setenv("FLASK_DEBUG", "True")
    assert os.getenv("FLASK_DEBUG") == "True"
    app = create_app()
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        res = app.test_client().get("/admin/user/")
        assert res.status_code == 200
    assert os.getenv("FLASK_DEBUG") == "True"


def test_admin_view_off(monkeypatch):
    """Test admin interface off"""
    monkeypatch.setenv("FLASK_CONFIG", "Test")
    monkeypatch.setenv("FLASK_DEBUG", "False")
    assert os.getenv("FLASK_DEBUG") == "False"
    app = create_app()
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        res = app.test_client().get("/admin/user/")
        assert res.status_code == 404
    assert os.getenv("FLASK_DEBUG") == "False"


# With 'RequestMethods' class from mykro_common .. not needed?
# class TestAdminView(RequestMethods):
#     def test_admin_view_on(self, monkeypatch):
#         """Test admin interface on"""
#         monkeypatch.setenv("FLASK_CONFIG", "Test")
#         monkeypatch.setenv("FLASK_DEBUG", "True")
#         assert os.getenv("FLASK_DEBUG") == "True"
#         app = create_app()
#         with app.app_context():
#             self.client = app.test_client()
#             db.session.remove()
#             db.drop_all()
#             db.create_all()
#             res = self.get("/admin/user/")
#             assert res[1] == 200
#         assert os.getenv("FLASK_DEBUG") == "True"
#
#
#     def test_admin_view_off(self, monkeypatch):
#         """Test admin interface off"""
#         monkeypatch.setenv("FLASK_CONFIG", "Test")
#         monkeypatch.setenv("FLASK_DEBUG", "False")
#         assert os.getenv("FLASK_DEBUG") == "False"
#         app = create_app()
#         with app.app_context():
#             self.client = app.test_client()
#             db.session.remove()
#             db.drop_all()
#             db.create_all()
#             res = self.get("/admin/user/")
#             assert res[1] == 404
#         assert os.getenv("FLASK_DEBUG") == "False"
