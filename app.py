import streamlit as st
from transaction_processing import add_transaction, get_transactions
from budget_prediction import predict_budget
from user_auth import login_user, register_user, get_user_by_email
from bill_splitting import add_bill_split, get_bill_splits, mark_bill_paid, get_user_by_id
from budget_notifications import check_budget_alerts
from data_analysis import plot_expense_distribution,  plot_financial_overview, plot_saving_trend
from investment_tracking import add_investment, get_investments, get_total_invested
from db_connection import connect_db
from budget_management import set_budget, get_budget
from email_service import send_email
from income_management import add_income, get_income
from datetime import datetime
# from forex_python.converter import CurrencyRates

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="Personal Financial Tracker", layout="wide")

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None
# if "streak" not in st.session_state:
#     st.session_state["streak"] = 0

st.title("💰 Personal Financial Tracker")
menu = st.sidebar.radio("Menu", ["Home", "Transactions", "Budget", "Bill Splitting",   "Investments", "Income", "Savings", "Analytics", "Register/Login"])

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
elif menu == "Home":
    if st.session_state["user_id"]:
        st.subheader("Financial Overview")
        plot_financial_overview(st.session_state["user_id"])
    else:
        st.warning("Please log in to view your financial overview.")

elif menu == "Budget":
    if st.session_state["user_id"]:
        st.subheader("Manage Your Budget")
        
        category = st.selectbox("Select Category", ["Food", "Rent", "Shopping", "Transport", "Investment"])
        budget_amount = st.number_input("Set Budget Amount", min_value=0.01)
        
        if st.button("Save Budget"):
            set_budget(st.session_state["user_id"], category, budget_amount)
            st.success(f"Budget for {category} set to ₹{budget_amount}")

        # Display Current Budget
        current_budget = get_budget(st.session_state["user_id"], category)
        st.write(f"**Current Budget for {category}: ₹{current_budget}**")

        # Check Expenses vs Budget
        transactions = get_transactions(st.session_state["user_id"])
        investments = get_total_invested(st.session_state["user_id"])
        
        if category == "Investment":
            total_spent = investments
        else:
            total_spent = sum(t["amount"] for t in transactions if t["category"] == category)

        if total_spent > current_budget:
            st.warning(f"⚠️ Over Budget! (Spent: ₹{total_spent:.2f}, Budget: ₹{current_budget:.2f})")
            # Send email notification
            subject = "Budget Alert: Over Budget!"
            message = f"You have exceeded your budget for {category}. Spent: ₹{total_spent:.2f}, Budget: ₹{current_budget:.2f}"
            send_email(st.session_state["name"], subject, message)
        else:
            st.success(f"✅ Within Budget! (Spent: ₹{total_spent:.2f}, Budget: ₹{current_budget:.2f})")
    else:
        st.warning("Please log in to manage your budget.")

elif menu == "Transactions":
    if st.session_state["user_id"]:
        st.subheader("Add Transaction")
        amount = st.number_input("Amount", min_value=0.01)
        category = st.selectbox("Category", ["Food", "Rent", "Shopping", "Transport"])
        # currency = st.selectbox("Currency", ["USD", "INR", "EUR", "GBP"])
        # c = CurrencyRates()
        # converted_amount = c.convert(currency, "INR", amount)
        
        if st.button("Add"):
            add_transaction(st.session_state["user_id"], converted_amount, category)
            st.success("Transaction added!")
            # st.session_state["streak"] += 1  # Update spending streak
            # st.info(f"Current streak: {st.session_state['streak']} days")

        st.subheader("Your Transactions")
        transactions = get_transactions(st.session_state["user_id"])
        if transactions:
            st.table(transactions)
        else:
            st.warning("No transactions found.")
    else:
        st.warning("Please log in to view transactions.")
elif menu == "Bill Splitting":
    if st.session_state["user_id"]:
        st.subheader("Split a Bill")
        amount = st.number_input("Bill Amount", min_value=0.01)
        split_with_email = st.text_input("Friend’s Email")

        if st.button("Split Bill"):
            split_user = get_user_by_email(split_with_email)
            if split_user:
                split_user_id, split_user_name = split_user[0], split_user[1]
                add_bill_split(st.session_state["user_id"], amount, split_user_id)

                # Send email notification
                subject = "🔔 You have a new bill to split!"
                message = f"Hello {split_user_name},\n\nYou have a pending bill of ₹{amount} from {st.session_state['name']}. Please settle it soon!"
                if send_email(split_with_email, subject, message):
                    st.success(f"Bill split with {split_user_name}! Email sent successfully.")
                else:
                    st.warning("Bill added, but email could not be sent.")
            else:
                st.error("User not found!")

        st.subheader("Pending Bills")

        # ✅ Ensure this runs only when user is logged in
        bills = get_bill_splits(st.session_state["user_id"])

        if bills:
            for bill in bills:
                bill_receiver = get_user_by_id(bill["split_with"])  # Fetch user name by ID
                if bill_receiver:
                    receiver_name = bill_receiver[1]
                    st.write(f"🧾 ₹{bill['amount']} - Owed to {receiver_name}")

                    if st.button(f"Mark Paid {bill['id']}", key=f"paid_{bill['id']}"):
                        mark_bill_paid(bill["split_with"])
                        st.success(f"Bill of ₹{bill['amount']} marked as paid!")
                        st.rerun()  # Refresh UI
        else:
            st.warning("No pending bills.")
    else:
        st.warning("Please log in to manage bill splitting.")

elif menu == "Investments":
    if st.session_state["user_id"]:
        st.subheader("Track Your Investments")
        asset_name = st.text_input("Asset Name (e.g., Stocks, Crypto)")
        investment_amount = st.number_input("Invested Amount", min_value=0.01)
        current_value = st.number_input("Current Value", min_value=0.01)

        if st.button("Add Investment"):
            total_invested = float(get_total_invested(st.session_state["user_id"])) + investment_amount

            investment_budget = get_budget(st.session_state["user_id"], "Investment")
            
            if total_invested > investment_budget:
                st.error("❌ Investment exceeds budget! Reduce the amount.")
                # Send email notification
                subject = "Investment Alert: Over Budget!"
                message = f"Your total investments (₹{total_invested}) exceed your allocated budget of ₹{investment_budget}. Please adjust accordingly."
                send_email(st.session_state["name"], subject, message)
            else:
                add_investment(st.session_state["user_id"], asset_name, investment_amount, current_value)
                st.success("Investment Added!")
                # Send email confirmation
                subject = "Investment Confirmation"
                message = f"You have successfully invested ₹{investment_amount} in {asset_name}. Current Value: ₹{current_value}"
                send_email(st.session_state["name"], subject, message)

        st.subheader("Your Portfolio")
        investments = get_investments(st.session_state["user_id"])
        if investments:
            st.table(investments)
        else:
            st.warning("No investments recorded.")
    else:
        st.warning("Please log in to track investments.")

elif menu == "Income":
    if st.session_state["user_id"]:
        st.subheader("Manage Your Income")
        income_amount = st.number_input("Enter Income Amount", min_value=0.01)
        source = st.text_input("Income Source")
        if st.button("Add Income"):
            # Get the current date
            current_date = datetime.today().strftime('%Y-%m-%d')
            add_income(st.session_state["user_id"], income_amount, current_date, source)
            st.success("Income added!")
        
        st.subheader("Total Income")
        total_income = get_income(st.session_state["user_id"])
        formatted_income = [
             f"{date.strftime('%Y-%m-%d')}: ₹{amount:,.2f}" for date, amount in total_income]

        # Join entries into a readable string
        display_income = "\n".join(formatted_income)

        st.write(f"Total Income:\n{display_income}")
        
    else:
        st.warning("Please log in to manage your income.")

elif menu == "Savings":
    if st.session_state["user_id"]:
        st.subheader("Your Savings")

        # Extract total income as a number
        total_income = sum(amount for _, amount in get_income(st.session_state["user_id"]))

        # Fetch transactions
        transactions = get_transactions(st.session_state["user_id"])
        total_expense = sum(t["amount"] for t in transactions)

        # Fetch total investment
        total_investment = get_total_invested(st.session_state["user_id"])

        # Compute total savings
        total_savings = total_income - total_expense - total_investment

        # Display formatted total savings
        st.write(f"Total Savings: ₹{total_savings:,.2f}")

        # Plot savings trend
        plot_saving_trend(st.session_state["user_id"])
    else:
        st.warning("Please log in to view your savings.")

# elif menu == "AI Budgeting":
#     if st.session_state["user_id"] is None:
#         st.warning("Please log in to use AI-powered budgeting.")
#     else:
#         st.subheader("Predict Your Future Budget")
#         transactions = get_transactions(st.session_state["user_id"])
#         if transactions:
#             budget_model = train_budget_model(transactions)
#             predicted_budget = predict_budget(budget_model, len(transactions))
#             st.info(f"Predicted budget for next month: ${predicted_budget:.2f}")
#         else:
#             st.warning("Not enough data to predict.")

# elif menu == "Voice Commands":
#     st.subheader("Log Expense via Voice")
#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()
#     with mic as source:
#         st.info("Say your expense (e.g., '50 dollars on food')...")
#         audio = recognizer.listen(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         st.success(f"You said: {text}")
#         # Convert spoken text into a transaction (e.g., "50 dollars on food")
#         words = text.split()
#         amount = float(words[0])
#         category = words[-1]
#         add_transaction(st.session_state["user_id"], amount, category)
#         st.success("Transaction added!")
#     except Exception as e:
#         st.error("Could not understand audio")

elif menu == "Analytics":
    if st.session_state["user_id"]:
        st.subheader("Expense Breakdown")
        plot_expense_distribution(st.session_state["user_id"])
        st.subheader("Savings Trend")
        plot_saving_trend(st.session_state["user_id"])
    else:
        st.warning("Please log in to view analytics.")

# Budget Alerts
if st.session_state["user_id"]:
    alerts = check_budget_alerts(st.session_state["user_id"])
    if alerts:
        for alert in alerts:
            st.warning(alert)
