from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import Response
from flask import jsonify

from flaskr.auth.auth import auth
from flaskr.auth.queries import get_user_by_username
from flaskr.db import get_db
from flaskr.comment.queries import (
    create_comment, comment_list, get_comment,
    update_comment, delete_comment
)


bp = Blueprint("comment", __name__)

def check_comment(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """

    comment = get_comment(get_db(), id)
    if comment is None:
        abort(404, "Comment id {0} doesn't exist.".format(id))
    user  = get_user_by_username(db, request.authorization['username'])
    if check_author and comment["author_id"] != user["id"]:
        abort(403)

    return comment


@bp.route("/posts/<int:post_id>/comments/", methods=("GET", "POST"))
@auth.login_required
def create():
    """Create a new comment for the current user."""
    if request.method == "POST":
        error = None
        db = get_db()
        json_data = request.get_json()
        body = json_data['body']
        user = get_user_by_username(db, request.authorization['username'])
        create_comment(db, body, user['id'])
        return Response("Comment successfully created", status=200)
           
    return Response("Method is not POST",status=401)


@bp.route("/posts/<int:post_id>/comments/<int:id>/", methods=("GET", "POST"))
@auth.login_required
def update(id):
    """Update a post if the current user is the author."""
    comment = check_comment(id)

    if request.method == "POST":
        error = None
        db = get_db()
        json_data = request.get_json()
        body = json_data['body']
        update_post(db, body, id)
        return Response("Updated!", status=200)
            
    return Response("Method is not POST",status=400)


@bp.route("/posts/<int:post_id>/comments/<int:id>/", methods=("POST",))
@auth.login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    check_comment(id)
    db = get_db()
    delete_comment(db, id)
    return Response("Comment deleted", status=200)
