import hashlib
from db_connection import connect_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, email, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    sql = "INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, hashed_pw)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_pw = hash_password(password)
    sql = "SELECT id, name FROM Users WHERE email=%s AND password=%s"
    cursor.execute(sql, (email, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user
def get_user_by_email(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user