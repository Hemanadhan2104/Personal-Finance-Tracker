from db_connection import connect_db

def check_budget_alerts(user_id):
    conn = connect_db()
    sql = """
            SELECT t.user_id, COALESCE(SUM(b.budget_amount), 0) AS total_budget, COALESCE(SUM(t.amount), 0) AS total_spent
            FROM transactions t
            LEFT JOIN budgets b ON t.user_id = b.user_id
            WHERE t.user_id = %s
            GROUP BY t.user_id
    """


    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (user_id,))
    budgets = cursor.fetchall()
    conn.close()
    
    alerts = []
    for budget in budgets:
        if budget["total_spent"] > budget["total_budget"]:
            alerts.append(f"⚠️ Over Budget! (Spent: {budget['total_spent']}, Budget: {budget['total_budget']})")
    return alerts
