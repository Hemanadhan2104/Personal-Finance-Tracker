from db_connection import connect_db

def add_bill_split(payer_id, amount, split_with):
    """ Add a shared bill entry """
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO BillSplitting (payer_id, amount, split_with, status) VALUES (%s, %s, %s, 'pending')"
    cursor.execute(sql, (payer_id, amount, split_with))
    conn.commit()
    conn.close()



def get_bill_splits(user_id):
    """ Get pending shared expenses """
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM BillSplitting WHERE (payer_id = %s OR split_with = %s) AND status = 'pending'"
    cursor.execute(sql, (user_id, user_id))
    bills = cursor.fetchall()
    conn.close()
    return bills


def mark_bill_paid(bill_id):
    """ Mark a shared bill as paid """
    conn = connect_db()
    cursor = conn.cursor()
    sql = "UPDATE BillSplitting SET status = 'paid' WHERE id = %s"
    cursor.execute(sql, (bill_id,))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    """ Fetch user details by user ID from the database """
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT id, name FROM users WHERE id = %s"  # Ensure 'users' is the correct table name
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()  # Fetch the first result

    conn.close()
    return user 