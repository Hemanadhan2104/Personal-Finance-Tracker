import streamlit as st
from db_connection import connect_db
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from income_management import add_income, get_income
from transaction_processing import add_transaction, get_transactions
from investment_tracking import add_investment, get_investments, get_total_invested
def plot_expense_distribution(user_id):
    conn = connect_db()
    
    # ✅ Fetch all transactions (no type column)
    sql = "SELECT category, SUM(amount) AS total FROM Transactions WHERE user_id = %s GROUP BY category"
    
    data = pd.read_sql(sql, conn, params=(user_id,))
    conn.close()

    if not data.empty:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(data["total"], labels=data["category"], autopct='%1.1f%%', 
               colors=sns.color_palette("viridis", len(data)), startangle=140)
        ax.set_title("Expense Distribution")

        # ✅ Display in Streamlit
        st.pyplot(fig)
    else:
        st.warning("No transactions available for analysis.")

def plot_financial_overview(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    # ✅ Fetch total income from new Income table
    income_query = "SELECT SUM(amount) FROM Income WHERE user_id = %s"
    cursor.execute(income_query, (user_id,))
    total_income = cursor.fetchone()[0] or 0  # If NULL, set to 0

    # ✅ Fetch total expenses (Transactions table)
    expense_query = "SELECT SUM(amount) FROM Transactions WHERE user_id = %s"
    cursor.execute(expense_query, (user_id,))
    total_expense = cursor.fetchone()[0] or 0

    # ✅ Fetch total investments
    investment_query = "SELECT SUM(investment_amount) FROM Investments WHERE user_id = %s"
    cursor.execute(investment_query, (user_id,))
    total_investment = cursor.fetchone()[0] or 0

    conn.close()

    # ✅ Calculate savings properly
    savings = total_income - (total_expense + total_investment)
    if savings < 0:
        savings = 0  # Avoid showing negative savings

    # ✅ Prepare data for visualization
    financial_data = {
        "Category": ["Income", "Expenses", "Investments", "Savings"],
        "Total Amount": [total_income, total_expense, total_investment, savings]
    }
    
    df_financial = pd.DataFrame(financial_data)

    # ✅ **Pie Chart for Financial Overview** (Show only non-zero values)
    filtered_df = df_financial[df_financial["Total Amount"] > 0]

    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(filtered_df["Total Amount"], labels=filtered_df["Category"], autopct='%1.1f%%', 
               colors=sns.color_palette("coolwarm", len(filtered_df)), startangle=140)
        ax.set_title("Financial Overview")
        st.pyplot(fig)
    else:
        st.warning("No financial data available for visualization.")

    # ✅ **Bar Chart for Income, Expenses, Investments, and Savings**
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=df_financial["Category"], y=df_financial["Total Amount"], palette="coolwarm", ax=ax)
    ax.set_ylabel("Total (₹)")
    ax.set_title("Income vs. Expenses vs. Investments vs. Savings")
    
    # ✅ Display in Streamlit
    st.pyplot(fig)

def plot_saving_trend(user_id):
    # Fetch user income, expenses, and investments
    income_data = get_income(user_id)
    expenses = get_transactions(user_id)
    investments = get_total_invested(user_id)

    if not income_data:
        st.warning("No income data available!")
        return

    # Convert to DataFrame for easier manipulation
    df_income = pd.DataFrame(income_data, columns=["date", "amount"])
    df_expenses = pd.DataFrame(expenses, columns=["date", "amount"])
    
    # Group by date and sum values
    df_income = df_income.groupby("date")["amount"].sum().reset_index()
    df_expenses = df_expenses.groupby("date")["amount"].sum().reset_index()

    # Merge expenses with income data
    df = pd.merge(df_income, df_expenses, on="date", how="left").fillna(0)
    df["investments"] = investments  # Assuming static total investments for simplicity

    # Calculate savings: Income - (Expenses + Investments)
    df["savings"] = df["amount_x"] - (df["amount_y"] + df["investments"])
    
    # Plot the savings trend
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["savings"], marker="o", linestyle="-", color="g", label="Savings")
    plt.xlabel("Date")
    plt.ylabel("Savings Amount")
    plt.title("Savings Trend Over Time")
    plt.legend()
    plt.grid(True)
    
    # Display in Streamlit
    st.pyplot(plt)