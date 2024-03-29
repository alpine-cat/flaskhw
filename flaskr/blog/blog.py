from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask import Response
from werkzeug.exceptions import abort

from flaskr.auth.auth import auth
from flaskr.auth.queries import get_user_by_username
from flaskr.db import get_db
from flaskr.blog.queries import (
    create_post, delete_post, get_post, update_post, post_list
)

bp = Blueprint("blog", __name__)


def check_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """

    post = get_post(get_db(), id)
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/post", methods=("GET", "POST"))
@auth.login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        error = None
        db = get_db()
        json_data = request.get_json()
        title = json_data['title']
        body = json_data['body']
        user = get_user_by_username(db, request.authorization['username'])
        create_post(db, title, body, user['id'])
        return Response("Post successfully created", status=200)
        
    return Response("Method is not POST",status=401)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@auth.login_required
def update(id):
    """Update a post if the current user is the author."""
    post = check_post(id)

    if request.method == "POST":
        error = None
        db = get_db()
        json_data = request.get_json()
        title = json_data['title']
        body = json_data['body']
        update_post(db, title, body, id)
        return Response("Updated!", status=200)
       
    return Response("Method is not POST",status=40)


@bp.route("/<int:id>/delete", methods=("POST",))
@auth.login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    check_post(id)
    db = get_db()
    delete_post(db, id)
    return Response("Post deleted",status=200)
