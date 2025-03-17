from db_connection import connect_db

def add_transaction(user_id, amount, category, currency="INR"):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Transactions (user_id, amount, category, currency, date) VALUES (%s, %s, %s, %s, NOW())"
    values = (user_id, amount, category, currency)
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT amount, category, date FROM Transactions WHERE user_id = %s ORDER BY date DESC"
    cursor.execute(sql, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions
