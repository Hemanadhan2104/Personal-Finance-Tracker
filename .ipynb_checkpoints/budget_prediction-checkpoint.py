import pandas as pd
from sklearn.linear_model import LinearRegression

def predict_budget(user_id):
    conn = connect_db()
    sql = f"SELECT amount, category FROM Transactions WHERE user_id = {user_id}"
    data = pd.read_sql(sql, conn)
    conn.close()

    if data.empty:
        return 0

    X = pd.get_dummies(data['category'])
    y = data['amount']

    model = LinearRegression()
    model.fit(X, y)

    predicted_budget = model.predict([X.iloc[-1]])[0]
    return round(predicted_budget, 2)
