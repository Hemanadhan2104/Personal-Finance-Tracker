import streamlit as st
from backend.transaction_processing import add_transaction, get_transactions
from backend.budget_prediction import predict_budget
from backend.user_auth import login_user, register_user

st.set_page_config(page_title="Personal Financial Tracker", layout="wide")

st.title("💰 Personal Financial Tracker")
menu = st.sidebar.radio("Menu", ["Home", "Transactions", "Budget", "Register/Login"])

if menu == "Register/Login":
    st.subheader("Register / Login")
    choice = st.radio("Choose an option", ["Login", "Register"])
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if choice == "Register":
        name = st.text_input("Full Name")
        if st.button("Register"):
            register_user(name, email, password)
            st.success("Registered successfully! You can now log in.")

    elif choice == "Login":
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state["user_id"] = user[0]
                st.session_state["name"] = user[1]
                st.success(f"Welcome, {user[1]}!")
            else:
                st.error("Invalid credentials")

elif menu == "Transactions":
    st.subheader("Add Transaction")
    amount = st.number_input("Amount", min_value=0.01)
    category = st.selectbox("Category", ["Food", "Rent", "Shopping", "Transport"])
    if st.button("Add"):
        add_transaction(st.session_state["user_id"], amount, category)
        st.success("Transaction added!")

    st.subheader("Your Transactions")
    transactions = get_transactions(st.session_state["user_id"])
    if transactions:
        st.table(transactions)
    else:
        st.warning("No transactions found.")
elif menu == "Bill Splitting":
    st.subheader("Split a Bill")
    amount = st.number_input("Bill Amount", min_value=0.01)
    split_with = st.text_input("Friend’s Email")
    
    if st.button("Split Bill"):
        user_id = st.session_state["user_id"]
        split_user = get_user_by_email(split_with)
        if split_user:
            add_bill_split(user_id, amount, split_user[0])
            st.success("Bill Split Added!")
        else:
            st.error("User not found!")

    st.subheader("Pending Bills")
    bills = get_bill_splits(st.session_state["user_id"])
    if bills:
        for bill in bills:
            st.write(f"🧾 {bill['amount']} - Owed to {bill['split_with']}")
            if st.button(f"Mark Paid {bill['id']}"):
                mark_bill_paid(bill['id'])
                st.success("Bill marked as paid!")
elif menu == "Investments":
    st.subheader("Track Your Investments")
    asset_name = st.text_input("Asset Name (e.g., Stocks, Crypto)")
    investment_amount = st.number_input("Invested Amount", min_value=0.01)
    current_value = st.number_input("Current Value", min_value=0.01)
    
    if st.button("Add Investment"):
        add_investment(st.session_state["user_id"], asset_name, investment_amount, current_value)
        st.success("Investment Added!")

    st.subheader("Your Portfolio")
    investments = get_investments(st.session_state["user_id"])
    if investments:
        st.table(investments)
    else:
        st.warning("No investments recorded.")
elif menu == "Analytics":
    st.subheader("Expense Breakdown")
    user_id = st.session_state["user_id"]
    plot_expense_distribution(user_id)
alerts = check_budget_alerts(st.session_state["user_id"])
if alerts:
    for alert in alerts:
        st.warning(alert)
