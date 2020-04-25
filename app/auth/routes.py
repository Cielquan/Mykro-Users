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
    app.auth.routes
    ~~~~~~~~~~~~~~~

    Routes for 'auth' blueprint

    :copyright: (c) 2020 Christian Riedel
    :license: GPLv3, see LICENSE for more details
"""
from flask import request
from mykro_common.api_utils import ApiException, ApiResult, dataschema
from voluptuous import REMOVE_EXTRA, Schema

from ..auth import bp


@bp.route("/register", methods=["POST"])
@dataschema(Schema({}, extra=REMOVE_EXTRA,))
def register():
    post_data = request.get_json()
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")

    user = get_user_by_email(email)
    if user:
        auth_namespace.abort(400, "Sorry. That email already exists.")
    user = add_user(username, email, password)
    return user, 201


@bp.route("/login", methods=["POST"])
@dataschema(Schema({}, extra=REMOVE_EXTRA,))
def login():
    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")
    response_object = {}

    user = get_user_by_email(email)
    if not user or not bcrypt.check_password_hash(user.password, password):
        auth_namespace.abort(404, "User does not exist")
    access_token = user.encode_token(user.id, "access")
    refresh_token = user.encode_token(user.id, "refresh")

    response_object = {
        "access_token": access_token.decode(),
        "refresh_token": refresh_token.decode(),
    }
    return response_object, 200


@bp.route("/refresh", methods=["POST"])
@dataschema(Schema({}, extra=REMOVE_EXTRA,))
def refresh():
    post_data = request.get_json()
    refresh_token = post_data.get("refresh_token")
    response_object = {}

    try:
        resp = User.decode_token(refresh_token)
        user = get_user_by_id(resp)
        if not user:
            auth_namespace.abort(401, "Invalid token")
        access_token = user.encode_token(user.id, "access")
        refresh_token = user.encode_token(user.id, "refresh")

        response_object = {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode(),
        }
        return response_object, 200
    except jwt.ExpiredSignatureError:
        auth_namespace.abort(401, "Signature expired. Please log in again.")
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        auth_namespace.abort(401, "Invalid token. Please log in again.")
    """
    Generate an access token for the user.
    This endpoint is requires basic auth with nickname and password.
    """
    return jsonify({"token": generate_token(g.current_user["id"])})


@bp.route("/status", methods=["GET"])
def status():
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            access_token = auth_header.split(" ")[1]
            resp = User.decode_token(access_token)
            user = get_user_by_id(resp)
            if not user:
                auth_namespace.abort(401, "Invalid token")
            return user, 200
        except jwt.ExpiredSignatureError:
            auth_namespace.abort(401, "Signature expired. Please log in again.")
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            auth_namespace.abort(401, "Invalid token. Please log in again.")
    else:
        auth_namespace.abort(403, "Token required")


#######################################
@app.route("/api/tokens", methods=["DELETE"])
# TODO 23.02.2020: like logout; add refresh token with ttl ot redis/etcd
@token_auth.login_required
def revoke_token():
    """
    Revoke a user token.
    This endpoint is requires a valid user token.
    """
    # get the token from the Authorization header
    token = request.headers["Authorization"].split()[1]

    # calculate the time this token has left (add 5s for safety)
    ttl = g.jwt_claims["exp"] - int(time.time()) + 5

    if ttl > 0:
        etcd = etcd_client()
        etcd.write("/revoked-tokens/" + token, "", ttl=ttl)
    return "", 204
