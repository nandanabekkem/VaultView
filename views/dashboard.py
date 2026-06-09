import streamlit as st
import pandas as pd
from db.database import get_connection


def get_summary(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, category, amount, date
        FROM transactions
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0, 0, 0, None

    df = pd.DataFrame(rows, columns=["type", "category", "amount", "date"])
    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    balance = total_income - total_expense
    return total_income, total_expense, balance, df


def show_dashboard():
    st.markdown("<h3 style='color:#1a1a1a; margin-bottom:1rem;'>Overview</h3>", unsafe_allow_html=True)

    user_id = st.session_state.user_id
    total_income, total_expense, balance, df = get_summary(user_id)

    # ── METRIC CARDS ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💵 Total Income", value=f"₹{total_income:,.2f}")
    with col2:
        st.metric(label="💸 Total Expenses", value=f"₹{total_expense:,.2f}")
    with col3:
        st.metric(label="🏦 Balance", value=f"₹{balance:,.2f}", delta=f"₹{balance:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    if df is None or df.empty:
        st.info("No transactions yet! Head to 💸 Transactions to add some.")
        return

    # ── TWO COLUMN LAYOUT ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem; margin-bottom:12px;">
            <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:12px;">📅 Monthly Spending</p>
        """, unsafe_allow_html=True)

        df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
        monthly = df[df["type"] == "expense"].groupby("month")["amount"].sum().reset_index()

        if not monthly.empty:
            st.bar_chart(monthly.set_index("month")["amount"], color="#1D9E75")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem;">
            <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:8px;">🕐 Recent Transactions</p>
        """, unsafe_allow_html=True)

        recent = df.sort_values("date", ascending=False).head(5)

        for _, row in recent.iterrows():
            color = "#1D9E75" if row["type"] == "income" else "#D85A30"
            sign = "+" if row["type"] == "income" else "-"
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;
                        padding:8px 0; border-bottom:1px solid #f0f0f0;">
                <div>
                    <span style="font-size:13px; font-weight:500; color:#1a1a1a;">{row['category']}</span><br>
                    <span style="font-size:11px; color:#aaa;">{row['date']}</span>
                </div>
                <span style="font-size:14px; font-weight:500; color:{color};">
                    {sign}₹{row['amount']:,.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)