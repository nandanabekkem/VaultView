import streamlit as st
import pandas as pd
from db.database import get_connection


def get_all_transactions(user_id):
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

    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["ID", "Type", "Category", "Amount", "Note", "Date"])
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def show_history():
    st.markdown("<h3 style='color:#1a1a1a; margin-bottom:1rem;'>History</h3>", unsafe_allow_html=True)

    user_id = st.session_state.user_id
    df = get_all_transactions(user_id)

    if df is None:
        st.info("No transactions yet! Add some from 💸 Transactions")
        return

    # ── FILTERS ──
    st.markdown("""
    <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem; margin-bottom:1rem;">
        <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:0.5rem;">🔍 Filter Transactions</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        type_filter = st.selectbox("Type", ["All", "income", "expense"])
    with col2:
        all_categories = ["All"] + sorted(df["Category"].unique().tolist())
        category_filter = st.selectbox("Category", all_categories)
    with col3:
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        all_months = ["All"] + sorted(df["Month"].unique().tolist(), reverse=True)
        month_filter = st.selectbox("Month", all_months)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── APPLY FILTERS ──
    filtered_df = df.copy()

    if type_filter != "All":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]
    if month_filter != "All":
        filtered_df = filtered_df[filtered_df["Month"] == month_filter]

    # ── SUMMARY ──
    col1, col2, col3 = st.columns(3)
    total_in = filtered_df[filtered_df["Type"] == "income"]["Amount"].sum()
    total_out = filtered_df[filtered_df["Type"] == "expense"]["Amount"].sum()
    net = total_in - total_out

    with col1:
        st.metric("💵 Income", f"₹{total_in:,.2f}")
    with col2:
        st.metric("💸 Expenses", f"₹{total_out:,.2f}")
    with col3:
        st.metric("🏦 Net", f"₹{net:,.2f}", delta=f"₹{net:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABLE ──
    if filtered_df.empty:
        st.warning("No transactions match your filters!")
        return

    st.markdown(f"<p style='font-size:13px; color:#888; margin-bottom:0.5rem;'>Showing {len(filtered_df)} records</p>", unsafe_allow_html=True)

    display_df = filtered_df.drop(columns=["ID", "Month"]).copy()

    # Format columns
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
    display_df["Date"] = display_df["Date"].dt.strftime("%d %b %Y")
    display_df["Note"] = display_df["Note"].fillna("—")

    # Apply color styling to Type column
    def color_type(val):
        color = "#1D9E75" if val == "income" else "#D85A30"
        return f"color: {color}; font-weight: 500"

    styled_df = display_df.style.map(color_type, subset=["Type"])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── DOWNLOAD ──
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="vaultview_history.csv",
        mime="text/csv"
    )