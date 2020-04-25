# ======================================================================================
# Copyright (c) 2020 Christian Riedel
#
# This file 'routes.py' created 2020-02-22
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
    app.users.routes
    ~~~~~~~~~~~~~~~~

    Routes for 'users' blueprint

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
from flask import request
from mykro_common.api_utils import ApiException, ApiResult, dataschema
from voluptuous import REMOVE_EXTRA, Schema

from ..users import bp


@bp.route("/", methods=["GET"])
def get_users():
    """Returns all users."""
    return get_all_users(), 200
    """
    Return list of users.
    This endpoint is publicly available, but if the client has a token it
    should send it, as that indicates to the server that the user is online.
    """
    users = User.query.order_by(User.updated_at.asc(), User.nickname.asc())
    if request.args.get("online"):
        users = users.filter_by(online=(request.args.get("online") != "0"))
    if request.args.get("updated_since"):
        users = users.filter(User.updated_at >= int(request.args.get("updated_since")))
    return jsonify({"users": [user.to_dict() for user in users.all()]})


@bp.route("/", methods=["POST"])
@dataschema(
    Schema(
        {"username": str, "password": str, "password2": str, "email": str},
        extra=REMOVE_EXTRA,
    )
)
def create_user():
    """Creates a new user."""
    post_data = request.get_json()
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    response_object = {}

    user = get_user_by_email(email)
    if user:
        response_object["message"] = "Sorry. That email already exists."
        return response_object, 400
    add_user(username, email, password)
    response_object["message"] = f"{email} was added!"
    return response_object, 201
    #######################
    """
    Register a new user.
    This endpoint is publicly available.
    """
    user = User.create(request.get_json() or {})
    if User.query.filter_by(nickname=user.nickname).first() is not None:
        abort(400)
    db.session.add(user)
    db.session.commit()
    r = jsonify(user.to_dict())
    r.status_code = 201
    r.headers["Location"] = url_for("get_user", id=user.id)
    return r


@bp.route("/<int:id>", methods=["GET"])
def get_user():
    """Returns a single user."""
    user = get_user_by_id(user_id)
    if not user:
        users_namespace.abort(404, f"User {user_id} does not exist")
    return user, 200
    """
    Return a user.
    This endpoint is publicly available, but if the client has a token it
    should send it, as that indicates to the server that the user is online.
    """
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route("/<int:id>", methods=["PUT"])
def change_user():
    """Updates a user."""
    post_data = request.get_json()
    username = post_data.get("username")
    email = post_data.get("email")
    response_object = {}

    user = get_user_by_id(user_id)
    if not user:
        users_namespace.abort(404, f"User {user_id} does not exist")
    update_user(user, username, email)
    response_object["message"] = f"{user.id} was updated!"
    return response_object, 200
    """
    Modify an existing user.
    This endpoint requires a valid user token.
    Note: users are only allowed to modify themselves.
    """
    user = User.query.get_or_404(id)
    if user.id != g.jwt_claims["user_id"]:
        abort(403)
    user.from_dict(request.get_json() or {})
    db.session.add(user)
    db.session.commit()
    return "", 204


@bp.route("/<int:id>", methods=["DELETE"])
def delete_user():
    """Updates a user."""
    response_object = {}
    user = get_user_by_id(user_id)
    if not user:
        users_namespace.abort(404, f"User {user_id} does not exist")
    delete_user(user)
    response_object["message"] = f"{user.email} was removed!"
    return response_object, 200


################################
@app.route("/api/users/me", methods=["GET"])
@basic_auth.login_required
def get_me_user():
    """
    Return the authenticated user.
    This endpoint requires basic auth with nickname and password.
    """
    return jsonify(g.current_user.to_dict())


@app.route("/api/users/me", methods=["PUT"])
@token_auth.login_required
def set_user_online():
    """Set the user that owns the token online."""
    user = User.query.get(g.jwt_claims["user_id"])
    if user is not None:
        user.ping()
        db.session.commit()
    return "", 204


@app.route("/api/users/me", methods=["DELETE"])
@token_auth.login_required
def set_user_offline():
    """Set the user that owns the token offline."""
    user = User.query.get(g.jwt_claims["user_id"])
    if user is not None:
        user.online = False
        db.session.commit()
    return "", 204


################################
################################


@bp.route("/add", methods=["POST"])
@dataschema(
    Schema(
        {"username": str, "password": str, "password2": str, "email": str},
        extra=REMOVE_EXTRA,
    )
)
def add_numbers():
    a = request.args("a", type=int)
    b = request.args("b", type=int)
    if a is None or b is None:
        raise ApiException("Numbers must be integers")
    return ApiResult({"sum": a + b})
