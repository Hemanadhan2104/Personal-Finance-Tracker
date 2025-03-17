from db_connection import connect_db

def get_income(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT date, amount FROM income WHERE user_id = %s ORDER BY date"
    cursor.execute(query, (user_id,))
    income_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return income_data
def add_income(user_id, amount, date, source):
    conn = connect_db()
    cursor = conn.cursor()

    query = "INSERT INTO income (user_id, amount, date, source) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, amount, date, source))

    conn.commit()
    cursor.close()
    conn.close()