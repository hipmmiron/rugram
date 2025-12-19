import uuid
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

def register(username, password, avatar, handle):
    db = get_db()
    handle = handle.strip()
    if not handle:
        return None, "Handle не может быть пустым"
    username = username.strip()
    if not username:
        return None, "Имя не может быть пустым"
    try:
        uid = str(uuid.uuid4())
        pw = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (uid, username, handle, password, avatar) VALUES (?, ?, ?, ?, ?)",
            (uid, username, handle, pw, avatar)
        )
        db.commit()
        user = db.execute("SELECT * FROM users WHERE uid=?", (uid,)).fetchone()
        return dict(user), None
    except sqlite3.IntegrityError:
        return None, "Handle уже занят"

def login(handle_or_username, password):
    db = get_db()
    if handle_or_username.startswith('@'):
        row = db.execute("SELECT * FROM users WHERE handle=?", (handle_or_username,)).fetchone()
    else:
        row = db.execute("SELECT * FROM users WHERE username=?", (handle_or_username,)).fetchone()
    if row and check_password_hash(row["password"], password):
        return dict(row)
    return None

def get_user_by_id(uid):
    db = get_db()
    r = db.execute("SELECT * FROM users WHERE uid=?", (uid,)).fetchone()
    return dict(r) if r else None

def get_user_row_by_id(id_):
    db = get_db()
    return db.execute("SELECT * FROM users WHERE id=?", (id_,)).fetchone()
