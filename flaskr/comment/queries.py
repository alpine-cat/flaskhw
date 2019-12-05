def comment_list(db):
    return db.execute(
        "SELECT comment.id, body, created, post_id, author_id, username"
        " FROM comment INNER JOIN user"
        " ON comment.author_id = user.id"
        " WHERE post_id = ?"
        " ORDER BY created DESC"
    ).fetchall()

def get_comment(db, id):
    return db.execute(
            "SELECT comment.id, body, created, author_id, username"
            " FROM comment JOIN user ON comment.author_id = user.id"
            " WHERE comment.id = ?",
            (id,),
        ).fetchone()


def create_comment(db, body, author_id, post_id):
    db.execute(
        "INSERT INTO comment (body, author_id, post_id) VALUES (?, ?, ?)",
        (body, author_id, post_id),
    )
    db.commit()


def update_comment(db, body, id):
    db.execute(
        "UPDATE comment SET body = ? where id=?",
        (body, id)
    )
    db.commit()


def delete_comment(db, id):
    db.execute("DELETE FROM comment WHERE id = ?", (id,))
    db.commit()
