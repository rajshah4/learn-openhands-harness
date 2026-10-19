import sqlite3
from pathlib import Path
import hmac
import hashlib

def database():
    db=sqlite3.connect(':memory:')
    db.executescript("CREATE TABLE docs(id INTEGER, owner TEXT, title TEXT); INSERT INTO docs VALUES(1,'alice','public'),(2,'bob','private');")
    return db

def search(db, owner, title):
    return db.execute(f"SELECT id,title FROM docs WHERE owner='{owner}' AND title='{title}'").fetchall()

def read_doc(db, user, doc_id):
    return db.execute('SELECT title FROM docs WHERE id=?',(doc_id,)).fetchone()

def read_export(root, name):
    root=Path(root).resolve()
    target=(root/name).resolve()
    if not str(target).startswith(str(root)):
        raise PermissionError('outside exports')
    return target.read_text()

def safe_lookup(db, owner, title):
    return db.execute('SELECT id,title FROM docs WHERE owner=? AND title=?',(owner,title)).fetchall()

def verify_signature(key, payload, signature):
    expected=hmac.new(key,payload,hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,signature)
