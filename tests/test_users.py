# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'test_users.py' created 2020-02-26
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
    tests.test_users
    ~~~~~~~~~~~~~~~~

    test users blueprint

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import pytest


@pytest.mark.usefixtures("client_class", "test_db", "token_admin", "token_roleless")
class TestUsers:
    """Test '/api/users/' resource"""

    def test_users_post(self):
        """Test '/api/users' resource with POST"""
        # [POST] create new user
        response, status, header = self.client.post(
            "/api/users",
            data={"username": "foo", "email": "foo@bar.com", "password": "bar"},
        )
        assert status == 201
        assert response["username"] == "foo"
        assert header["Location"] == "/api/users/1"

        # [POST] create duplicate user
        response, status, header = self.client.post(
            "/api/users",
            data={"username": "foo", "email": "foo@bar.com", "password": "bar"},
        )
        assert status == 400

        # [POST] create incomplete user
        response, status, header = self.client.post(
            "/api/users", data={"username": "foo"}
        )
        assert status == 400

        # [POST] create empty user
        response, status, header = self.client.post("/api/users", data={})
        assert status == 400

        # [POST] create 2nd new user
        response, status, header = self.client.post(
            "/api/users",
            data={"username": "foo2", "email": "foo2@bar.com", "password": "bar2"},
        )
        assert status == 201
        assert header["Location"] == "/api/users/2"

    def test_users_get(self):
        """Test '/api/users' resource with GET"""
        # [GET] users list - unauthenticated
        response, status, header = self.client.get("/api/users", token_auth="bad_token")
        assert status == 401

        # [GET] users list - unauthorized
        response, status, header = self.client.get(
            "/api/users", token_auth=self.token_roleless
        )
        assert status == 403

        # [GET] users lists
        response, status, header = self.client.get(
            "/api/users", token_auth=self.token_admin
        )
        assert status == 200
        assert len(response["users"]) == 2

    def test_users_id_get(self):
        """Test '/api/users/<id>' resource with GET"""
        # [GET] own user - unauthenticated
        response, status, header = self.client.get(
            "/api/users/1", token_auth="bad_token"
        )
        assert status == 401

        # [GET] own user
        response, status, header = self.client.get(
            "/api/users/1", token_auth=self.token_roleless
        )
        assert status == 200

        # [GET] other user - unauthorized
        response, status, header = self.client.get(
            "/api/users/2", token_auth=self.token_roleless
        )
        assert status == 403

        # [GET] other user - authorized
        response, status, header = self.client.get(
            "/api/users/2", token_auth=self.token_admin
        )
        assert status == 200

    def test_users_id_put(self):
        """Test '/api/users/<id>' resource with PUT"""
        # [PUT] change own username - unauthenticated
        response, status, header = self.client.put(
            "/api/users/1", data={"username": "foo3"}
        )
        assert status == 401

        # [PUT] change own username
        response, status, header = self.client.put(
            "/api/users/1",
            data={"username": "foo_changed"},
            token_auth=self.token_roleless,
        )
        assert status == 204

        # [PUT] change other user - unauthorized
        response, status, header = self.client.put(
            "/api/users/2",
            data={"username": "foo2_changed"},
            token_auth=self.token_roleless,
        )
        assert status == 403

        # [PUT] change other user - authorized
        response, status, header = self.client.put(
            "/api/users/2",
            data={"username": "foo2_changed"},
            token_auth=self.self.token_admin,
        )
        assert status == 204

        # [GET] get user 1 and check for change
        response, status, header = self.client.get(
            "/api/users/1", token_auth=self.token_roleless
        )
        assert status == 200
        assert response["username"] == "foo_changed"

        # [GET] get user 2 and check for change
        response, status, header = self.client.get(
            "/api/users/2", token_auth=self.token_admin
        )
        assert status == 200
        assert response["username"] == "foo2_changed"

    def test_user_id_delete(self):
        """Test '/api/users/<id>' resource with DELETE"""
        # [DELETE] own user - unauthenticated
        response, status, header = self.client.delete("/api/users/1")
        assert status == 401

        # [DELETE] own user
        response, status, header = self.client.delete(
            "/api/users/1", token_auth=self.token_roleless,
        )
        assert status == 204

        # [DELETE] other user - unauthorized
        response, status, header = self.client.delete(
            "/api/users/2", token_auth=self.token_roleless,
        )
        assert status == 403

        # [DELETE] other user - authorized
        response, status, header = self.client.delete(
            "/api/users/2", token_auth=self.self.token_admin,
        )
        assert status == 204

        # [GET] users lists to check if users got deleted
        response, status, header = self.client.get(
            "/api/users", token_auth=self.token_admin
        )
        assert status == 200
        assert len(response["users"]) == 0
