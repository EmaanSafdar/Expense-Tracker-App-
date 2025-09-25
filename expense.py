import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Personal Expense Tracker with Budget Alert")

# Session state
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# Input section
with st.form("entry_form"):
    col1, col2 = st.columns(2)

    with col1:
        entry_type = st.selectbox("Type", ["Income", "Expense"])
        category = st.selectbox("Category", ["Salary", "Food", "Transport", "Shopping", "Other"])

    with col2:
        amount = st.number_input("Amount (PKR)", min_value=0.0, step=10.0)
        date = st.date_input("Date")

    note = st.text_input("Optional Note")
    submitted = st.form_submit_button("Add Entry")

    if submitted and amount > 0:
        st.session_state.transactions.append({
            "Date": date,
            "Type": entry_type,
            "Category": category,
            "Amount": amount,
            "Note": note
        })
        st.success("Entry added successfully!")

# Convert to DataFrame
df = pd.DataFrame(st.session_state.transactions)

if not df.empty:
    st.subheader("📊 Summary")
    income = df[df['Type'] == 'Income']['Amount'].sum()
    expenses = df[df['Type'] == 'Expense']['Amount'].sum()
    balance = income - expenses

    st.metric("💵 Total Income", f"PKR {income:,.0f}")
    st.metric("💸 Total Expenses", f"PKR {expenses:,.0f}")
    st.metric("🧾 Balance", f"PKR {balance:,.0f}")

    budget_limit = st.number_input("Set Your Monthly Budget (PKR)", min_value=1000.0, value=50000.0, step=500.0)
    if expenses > budget_limit:
        st.error(f"🚨 Alert: You've exceeded your monthly budget of PKR {budget_limit:,.0f}!")

    # Expense breakdown chart
    st.subheader("📍 Expense Breakdown by Category")
    expense_df = df[df['Type'] == 'Expense'].groupby("Category")['Amount'].sum()
    if not expense_df.empty:
        fig, ax = plt.subplots()
        expense_df.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    # Show full table
    st.subheader("📄 All Transactions")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

else:
    st.info("Add your first income or expense entry to begin tracking.")
