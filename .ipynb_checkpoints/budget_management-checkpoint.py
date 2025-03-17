from db_connection import connect_db

def set_budget(user_id, category, amount):
    """Sets or updates a budget for a specific category."""
    conn = connect_db()
    cursor = conn.cursor()

    # Check if a budget exists
    cursor.execute("SELECT id FROM Budgets WHERE user_id = %s AND category = %s", (user_id, category))
    existing_budget = cursor.fetchone()

    if existing_budget:
        # Update existing budget
        cursor.execute("UPDATE Budgets SET budget_amount = %s WHERE user_id = %s AND category = %s",
                       (amount, user_id, category))
    else:
        # Insert new budget
        cursor.execute("INSERT INTO Budgets (user_id, category, budget_amount) VALUES (%s, %s, %s)",
                       (user_id, category, amount))
    
    conn.commit()
    conn.close()

def get_budget(user_id, category):
    """Retrieves the budget for a specific category."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT budget_amount FROM Budgets WHERE user_id = %s AND category = %s", (user_id, category))
    budget = cursor.fetchone()
    conn.close()
    return budget[0] if budget else 0.00  # Default to 0 if no budget is found
