import streamlit as st
from db.database import get_connection
from datetime import date

INCOME_CATEGORIES = [
    "Salary", "Freelance", "Business", "Investment Returns",
    "Gift Received", "Other Income"
]

EXPENSE_CATEGORIES = [
    "Food & Dining", "Rent", "Transport", "Shopping",
    "Entertainment", "Savings", "Investment", "Insurance",
    "Give Away / Donations", "Medical", "Education", "Other Expense"
]


def add_transaction(user_id, trans_type, category, amount, note, trans_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, type, category, amount, note, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, trans_type, category, amount, note, str(trans_date)))
    conn.commit()
    conn.close()


def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()


def get_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, category, amount, note, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def show_transactions():
    st.markdown("<h3 style='color:#1a1a1a; margin-bottom:1rem;'>Transactions</h3>", unsafe_allow_html=True)

    user_id = st.session_state.user_id

    # ── ADD FORM ──
    st.markdown("""
    <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1.25rem; margin-bottom:1.5rem;">
        <p style="font-size:14px; font-weight:500; color:#1D9E75; margin-bottom:1rem;">➕ Add New Transaction</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        trans_type = st.selectbox("Transaction Type", ["Income", "Expense"])
    with col2:
        if trans_type == "Income":
            category = st.selectbox("Category", INCOME_CATEGORIES)
        else:
            category = st.selectbox("Category", EXPENSE_CATEGORIES)

    col3, col4 = st.columns(2)
    with col3:
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01, format="%.2f")
    with col4:
        trans_date = st.date_input("Date", value=date.today())

    note = st.text_input("Note (optional)", placeholder="e.g. Paid electricity bill")

    if st.button("Add Transaction ✅", use_container_width=True):
        if amount <= 0:
            st.error("Amount must be greater than 0!")
        else:
            add_transaction(user_id, trans_type.lower(), category, amount, note, trans_date)
            st.success(f"{trans_type} of ₹{amount:,.2f} added! 🎉")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── TRANSACTIONS LIST ──
    st.markdown("<p style='font-size:14px; font-weight:500; color:#555; margin-bottom:0.75rem;'>📋 Your Transactions</p>", unsafe_allow_html=True)

    rows = get_transactions(user_id)

    if not rows:
        st.info("No transactions yet! Add one above ☝️")
        return

    for row in rows:
        trans_id, trans_type, category, amount, note, trans_date = row
        color = "#1D9E75" if trans_type == "income" else "#D85A30"
        bg = "#f0faf5" if trans_type == "income" else "#fdf3f0"
        sign = "+" if trans_type == "income" else "-"
        icon = "🟢" if trans_type == "income" else "🔴"

        with st.expander(f"{icon}  {trans_date}  |  {category}  |  {sign}₹{amount:,.2f}"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"""
                <div style="background:{bg}; border-radius:8px; padding:0.75rem 1rem;">
                    <p style="margin:0 0 4px 0; font-size:13px;"><b>Type:</b> {trans_type.capitalize()}</p>
                    <p style="margin:0 0 4px 0; font-size:13px;"><b>Category:</b> {category}</p>
                    <p style="margin:0 0 4px 0; font-size:13px;"><b>Amount:</b> <span style="color:{color}; font-weight:500;">{sign}₹{amount:,.2f}</span></p>
                    <p style="margin:0 0 4px 0; font-size:13px;"><b>Date:</b> {trans_date}</p>
                    <p style="margin:0; font-size:13px;"><b>Note:</b> {note if note else "—"}</p>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️ Delete", key=f"del_{trans_id}"):
                    delete_transaction(trans_id)
                    st.success("Deleted!")
                    st.rerun()