# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'models.py' created 2020-02-22
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
    app.models
    ~~~~~~~~~~

    Database models for app

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
import os

from typing import Dict, List, TypeVar, Union

from flask import current_app
from mykro_common.api_utils import ApiException
from mykro_common.urls import url_for
from mykro_common.utils import timestamp

from app import bcrypt, db


User_T = TypeVar("User_T", bound="User")


class User(db.Model):
    """User database model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.Integer, default=timestamp, nullable=False)
    updated_at = db.Column(
        db.Integer, default=timestamp, onupdate=timestamp, nullable=False
    )

    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def password(self):
        """Non hashed password are not accessible"""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        """Create password hash"""
        self.password_hash = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        """Verify given password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def activate(self) -> None:
        """Activate user"""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate user"""
        self.active = False

    def from_dict(self, data: Dict[str, str], full_update: bool = False) -> None:
        """Import user data from a dictionary."""
        for field in {"username", "email", "password"}:
            try:
                setattr(self, field, data[field])
            except KeyError:
                if full_update:
                    raise ApiException(
                        "User could not be created/modified. "
                        f"Missing following data: {field}"
                    )

    def to_dict(self, include_email: bool = False) -> Dict[str, Union[str, int]]:
        """Export user to a dictionary."""
        data = {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "active": self.active,
            "_links": {  # TODO 26.02.2020: add links
                # "self": url_for("get_user", id=self.id),
            },
        }
        if include_email:
            data["email"] = self.email
        return data

    @staticmethod
    def add_user(*, username: str, email: str, password: str) -> User_T:
        """Create a new user."""
        user = User()
        user.from_dict(
            {"username": username, "email": email, "password": password},
            full_update=True,
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user: User_T, data: Dict[str, str]) -> User_T:
        """Modify a user."""
        user.from_dict(data, full_update=False)
        return user

    @staticmethod
    def delete_user(user: User_T) -> bool:
        """Delete given user"""
        db.session.delete(user)
        db.session.commit()
        return user

    @staticmethod
    def all_users() -> List[User_T]:
        """Get all users"""
        return User.query.all()

    @staticmethod
    def by_id(user_id: int) -> User_T:
        """Get user by given ID"""
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def by_username(username: str) -> User_T:
        """Get user by given username"""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def by_email(email: str) -> User_T:
        """Get user by given email"""
        return User.query.filter_by(email=email).first()
