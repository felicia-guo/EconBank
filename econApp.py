import streamlit as st
import pandas as pd
import hashlib
import json
import os
from datetime import datetime

# -------------------- CENTRALIZED DATA FILE --------------------
# Place this JSON in a shared folder or in the app folder on Streamlit Cloud
DATA_FILE = "economics_data.json"

# -------------------- LOAD AND SAVE FUNCTIONS --------------------
def load_data():
    """Load the central JSON file or create default admin account."""
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default admin account if file does not exist
        return {"users": {"admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(),
                                    "role": "admin",
                                    "logs": []}}}

def save_data():
    """Save current data to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE) or ".", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state['data'], f, indent=4)

# -------------------- SESSION STATE INIT --------------------
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()
if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None
if 'page' not in st.session_state:
    st.session_state['page'] = None

# -------------------- HELPER FUNCTIONS --------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log_transaction(user, t_type, amount, description):
    entry = {
        "type": t_type,
        "amount": float(amount),
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state['data']['users'][user]["logs"].append(entry)
    save_data()

def calculate_summary(user_logs):
    earned = sum(log["amount"] for log in user_logs if log["type"] == "Earned")
    spent = sum(log["amount"] for log in user_logs if log["type"] == "Spent")
    given = sum(log["amount"] for log in user_logs if log["type"] == "Given")
    received = sum(log["amount"] for log in user_logs if log["type"] == "Received")
    balance = earned + received - spent - given
    return earned, spent, given, received, balance

# -------------------- USER DASHBOARD --------------------
def user_dashboard(username):
    st.sidebar.title(f"Welcome, {username}")
    if st.sidebar.button("Log Out", key="logout_sidebar"):
        st.session_state['logged_in_user'] = None
        st.session_state['page'] = None
        st.rerun()  #mguo: force to login page immediately
        return

    if st.session_state['page'] == 'make_transaction':
        make_transaction_page(username)
        return

    tabs = st.tabs(["Summary", "Transactions", "Statistics"])

    # --- SUMMARY TAB ---
    with tabs[0]:
        logs = st.session_state['data']['users'][username]['logs']
        earned, spent, given, received, balance = calculate_summary(logs)

        st.markdown(f"""
        <div style='background-color:#9DD4FD; padding:15px; border-radius:10px; color:black'>
        <h4 style='color:#1E78BB;'>Summary</h4>
        <p><b>Earned:</b> ${earned:.2f}</p>
        <p><b>Spent:</b> ${spent:.2f}</p>
        <p><b>Given:</b> ${given:.2f}</p>
        <p><b>Received:</b> ${received:.2f}</p>
        <h4 style='color:#68B400;'>Balance: ${balance:.2f}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        if st.button("Make Transaction", key="summary_make_txn"):
            st.session_state['page'] = 'make_transaction'
            st.rerun()  #mguo

    # --- TRANSACTIONS TAB ---
    with tabs[1]:
        st.subheader("Transaction History")
        df_logs = pd.DataFrame(logs)
        if not df_logs.empty:
            st.dataframe(df_logs)
            st.bar_chart(df_logs.groupby("type")["amount"].sum())
        else:
            st.info("No transactions yet.")

        if st.button("Make Transaction", key="transactions_make_txn"):
            st.session_state['page'] = 'make_transaction'
            st.rerun()  #mguo

    # --- STATISTICS TAB ---
    with tabs[2]:
        st.subheader("Statistics")
        if logs:
            df_logs = pd.DataFrame(logs)
            df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
            st.line_chart(df_logs.groupby(df_logs['timestamp'].dt.date)['amount'].sum())
            st.bar_chart(df_logs.groupby("type")["amount"].sum())
        else:
            st.info("No data to display statistics.")

# -------------------- MAKE TRANSACTION PAGE --------------------
def make_transaction_page(username):
    st.header("💵 Make a Transaction")
    t_type = st.selectbox("Transaction Type", ["Earned", "Spent", "Given", "Received"], key="txn_type")
    amount = st.number_input("Amount", min_value=0.0, step=0.01, key="txn_amount")
    description = st.text_input("Description", key="txn_desc")

    if st.button("Submit Transaction", key="submit_txn"):
        if amount > 0:
            log_transaction(username, t_type, amount, description)
            st.success("Transaction added!")
            st.session_state['page'] = 'dashboard'
        else:
            st.error("Amount must be greater than 0.")

    if st.button("Back to Dashboard", key="back_dashboard"):
        st.session_state['page'] = 'dashboard'

# -------------------- ADMIN DASHBOARD --------------------
def admin_dashboard():
    st.sidebar.title("Admin Dashboard")
    if st.sidebar.button("Log Out", key="admin_logout_sidebar"):
        st.session_state['logged_in_user'] = None
        st.rerun()  #mguo: force to login page immediately
        return

    st.title("📈 Global Economic Overview")

    all_logs = []
    for user, data in st.session_state['data']['users'].items():
        for log in data['logs']:
            all_logs.append({"User": user, **log})

    if all_logs:
        df = pd.DataFrame(all_logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        st.subheader("All Transactions")
        st.dataframe(df.sort_values(by='timestamp', ascending=False))

        total_earned = df[df['type'] == 'Earned']['amount'].sum()
        total_spent = df[df['type'] == 'Spent']['amount'].sum()
        total_given = df[df['type'] == 'Given']['amount'].sum()
        total_received = df[df['type'] == 'Received']['amount'].sum()

        st.subheader("Summary Metrics")
        st.metric("Total Earned", f"${total_earned:.2f}")
        st.metric("Total Spent", f"${total_spent:.2f}")
        st.metric("Total Given", f"${total_given:.2f}")
        st.metric("Total Received", f"${total_received:.2f}")

        st.subheader("Transaction Trends Over Time")
        st.line_chart(df.groupby(df['timestamp'].dt.date)['amount'].sum())

        st.subheader("Transaction Breakdown by Type")
        st.bar_chart(df.groupby("type")["amount"].sum())

        st.subheader("Transactions per User")
        st.bar_chart(df.groupby("User")["amount"].sum())
    else:
        st.info("No transactions recorded yet.")

# -------------------- LOGIN PAGE --------------------
def login_page():
    st.title("💰 Economics Club Bank")
    st.markdown("<h3 style='color:#2E8B57;'>Login or Sign Up</h3>", unsafe_allow_html=True)

    choice = st.radio("Select an option", ["Login", "Sign Up"], horizontal=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login", key="login_button"):
            if username in st.session_state['data']['users'] and st.session_state['data']['users'][username]['password'] == hash_password(password):
                st.session_state['logged_in_user'] = username
                st.session_state['page'] = 'dashboard'
                st.success(f"Welcome back, {username}!")
                st.rerun()  #mguo: force page reload and go straight into dashboard
            else:
                st.error("Invalid username or password")
    else:  # Sign Up
        if st.button("Sign Up", key="signup_button"):
            if username.strip() == "" or password.strip() == "":
                st.error("Username and password cannot be empty")
            elif username in st.session_state['data']['users']:
                st.error("Username already exists")
            else:
                st.session_state['data']['users'][username] = {"password": hash_password(password),
                                                                "role": "user",
                                                                "logs": []}
                save_data()
                st.session_state['logged_in_user'] = username
                st.session_state['page'] = 'dashboard'
                st.success("Account created! Logging you in...")

# -------------------- MAIN APP --------------------
if st.session_state['logged_in_user'] is None:
    login_page()
else:
    role = st.session_state['data']['users'][st.session_state['logged_in_user']]['role']
    if role == "admin":
        admin_dashboard()
    else:
        user_dashboard(st.session_state['logged_in_user'])