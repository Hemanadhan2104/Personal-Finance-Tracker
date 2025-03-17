from db_connection import connect_db

def add_investment(user_id, asset_name, investment_amount, current_value):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO Investments (user_id, asset_name, investment_amount, current_value) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (user_id, asset_name, investment_amount, current_value))
    conn.commit()
    conn.close()

def get_investments(user_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM Investments WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    investments = cursor.fetchall()
    conn.close()
    return investments
def get_total_invested(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT SUM(investment_amount) FROM Investments WHERE user_id = %s"
    cursor.execute(sql, (user_id,))
    total = cursor.fetchone()[0] or 0  # Handle case when no investments exist
    conn.close()
    return total
