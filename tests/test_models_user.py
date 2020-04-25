# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'test_models_user.py' created 2020-02-23
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
    tests.test_models_user
    ~~~~~~~~~~~~~~~~~~~~~~

    test the User model

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import pytest

from mykro_common.api_utils import ApiException

from app.models import User


def test_password_get():
    """Test getting password attr"""
    user = User()
    with pytest.raises(AttributeError):
        assert user.password


def test_password_set_and_verify():
    """Test setting password attr and verifying password"""
    user = User()
    assert not user.password_hash
    user.password = "password"
    assert isinstance(user.password_hash, str)
    assert user.password_hash
    assert user.verify_password("password") is True
    assert user.verify_password("Password") is False


def test_from_dict():
    """Test adding data to User instance with dict"""
    user = User()
    assert not user.username
    assert not user.email
    assert not user.password_hash

    # Make failing full update (create)
    with pytest.raises(ApiException):
        assert user.from_dict(
            {"username": "user1", "email": "user1@test.com"}, full_update=True
        )
        assert user.from_dict({}, full_update=True)

    # Make full update (create)
    user.from_dict(
        {"username": "user2", "email": "user2@test.com", "password": "user2.pw"},
        full_update=True,
    )
    assert user.username == "user2"
    assert user.email == "user2@test.com"
    assert user.password_hash
    assert user.verify_password("user2.pw")

    # Make partial update (modify)
    user.from_dict({"username": "user3", "email": "user3@test.com"}, full_update=False)
    assert user.username == "user3"
    assert user.email == "user3@test.com"
    assert user.verify_password("user2.pw")


def test_add_user(test_db):
    """Test adding user to db"""
    #: Positive test
    user = User.add_user(username="user0", email="user0@test.com", password="user0.pw")
    assert user.username == "user0"
    assert user.email == "user0@test.com"
    assert user.password_hash
    assert user.verify_password("user0.pw")


def test_get_user_by_id(test_db):
    """Test getting user from db by id"""
    #: Negative test
    user = User.by_id(0)
    assert not user

    #: Positive test
    assert not User.by_id(1)
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")

    user = User.by_id(1)
    assert user.username == "user1"
    assert user.email == "user1@test.com"
    assert user.password_hash
    assert user.verify_password("user1.pw")


def test_get_user_by_username(test_db):
    """Test getting user from db by username"""
    #: Negative test
    user = User.by_username("")
    assert not user

    #: Positive test
    assert not User.by_username("user1")
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")

    user = User.by_username("user1")
    assert user.username == "user1"
    assert user.email == "user1@test.com"
    assert user.password_hash
    assert user.verify_password("user1.pw")


def test_get_user_by_email(test_db):
    """Test getting user from db by email"""
    #: Negative test
    user = User.by_email("")
    assert not user

    #: Positive test
    assert not User.by_email("user1@test.com")
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")

    user = User.by_email("user1@test.com")
    assert user.username == "user1"
    assert user.email == "user1@test.com"
    assert user.password_hash
    assert user.verify_password("user1.pw")


def test_to_dict(test_db):
    """Test getting user data"""
    assert not User.by_id(1)
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")
    user = User.by_id(1)

    #: w/o email
    data = user.to_dict(include_email=False)
    assert not data.get("email")

    #: w/ email
    data = user.to_dict(include_email=True)
    assert data["email"] == "user1@test.com"
    assert data["id"] == 1
    assert data["username"] == "user1"
    assert isinstance(data["created_at"], int)
    assert isinstance(data["updated_at"], int)
    assert data["active"] == True
    assert isinstance(data["_links"], dict)

    #: No password should be send
    assert not data.get("password")
    assert not data.get("password_hash")


def test_update_user(test_db):
    """Test modifying a user"""
    assert not User.by_id(1)
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")

    assert User.by_id(1).username == "user1"
    User.update_user(User.by_id(1), {"username": "user1_"})
    assert User.by_id(1).username == "user1_"


def test_active_state(test_db):
    """Test user's active state"""
    assert not User.by_id(1)
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")

    user = User.by_id(1)
    assert user.active is True
    user.deactivate()
    assert user.active is False
    user.activate()
    assert user.active is True


def test_delete_user(test_db):
    """Test deleting a user"""
    assert not User.by_id(1)
    User.add_user(username="user1", email="user1@test.com", password="user1.pw")

    user = User.by_id(1)
    assert user
    assert User.delete_user(user)
    assert not User.by_id(1)


def test_password_hashes_are_unique(test_db, add_user):
    """Test that equal password's hashes are unique"""
    assert not User.by_id(1)
    assert not User.by_id(2)
    user1 = add_user(username="user1", email="user1@test.com", password="same_pw")
    user2 = add_user(username="user2", email="user2@test.com", password="same_pw")
    assert user1.password_hash != user2.password_hash


def test_get_all_users(test_db, add_user):
    """Test getting all users"""
    assert not User.by_id(1)
    assert not User.by_id(2)
    add_user(username="user1", email="user1@test.com", password="user1.pw")
    add_user(username="user2", email="user2@test.com", password="user2.pw")

    users = User.all_users()
    assert len(users) == 2
    assert users == [User.by_id(1), User.by_id(2)]
