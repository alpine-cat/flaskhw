import functools
import json

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import Response
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth 


from flaskr.db import get_db
from flaskr.auth.queries import (
    create_user, get_user_by_id, get_user_by_username
)


bp = Blueprint("auth", __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    db = get_db()
    user = get_user_by_username(db, username)

    if user is None:
        return False
    return check_password_hash(user['password'], password)



@bp.route("/register", methods=("POST",))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    db = get_db()
    error = None

    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."
    elif get_user_by_username(db, username) is not None:
        error = "User {0} is already registered.".format(username)

    if error is None:
        create_user(db, username, password)
        user = get_user_by_username(db, username)
        register = {"user_id": user['id'], "username": user['username']}
        data = json.dumps(register)
        return Response(data, status=200)
        
    error = json.dumps({'error': error})
    return Response(error, status=400)


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return Response(response="Logged out", status=401)