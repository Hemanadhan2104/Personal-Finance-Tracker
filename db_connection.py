import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hemanadhan@2104",
        database="finance_tracker"
    )
    return conn
