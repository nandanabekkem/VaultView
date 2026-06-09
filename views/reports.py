import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db.database import get_connection


def get_data(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT type, category, amount, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["type", "category", "amount", "date"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def show_reports():
    st.markdown("<h3 style='color:#1a1a1a; margin-bottom:1rem;'>Reports</h3>", unsafe_allow_html=True)

    user_id = st.session_state.user_id
    df = get_data(user_id)

    if df is None:
        st.info("No data yet! Add some transactions first 💸")
        return

    # ── DATE FILTER ──
    st.markdown("""
    <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem; margin-bottom:1rem;">
        <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:0.5rem;">🗓️ Filter by Date Range</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From", value=df["date"].min())
    with col2:
        end_date = st.date_input("To", value=df["date"].max())

    st.markdown("</div>", unsafe_allow_html=True)

    df = df[
        (df["date"] >= pd.Timestamp(start_date)) &
        (df["date"] <= pd.Timestamp(end_date))
    ]

    if df.empty:
        st.warning("No transactions in this date range!")
        return

    df_expense = df[df["type"] == "expense"]
    df_income = df[df["type"] == "income"]

    # ── ROW 1: PIE + BAR ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
        <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem;">
            <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:0;">🥧 Expense Breakdown</p>
        """, unsafe_allow_html=True)

        if not df_expense.empty:
            expense_by_cat = df_expense.groupby("category")["amount"].sum().reset_index()
            fig_pie = px.pie(
                expense_by_cat,
                values="amount",
                names="category",
                hole=0.35,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_traces(textposition="inside", textinfo="percent+label")
            fig_pie.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                showlegend=False,
                height=280
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data!")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem;">
            <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:0;">📊 Monthly Income vs Expenses</p>
        """, unsafe_allow_html=True)

        df["month"] = df["date"].dt.to_period("M").astype(str)
        monthly = df.groupby(["month", "type"])["amount"].sum().reset_index()

        fig_bar = px.bar(
            monthly,
            x="month",
            y="amount",
            color="type",
            barmode="group",
            labels={"amount": "Amount (₹)", "month": "Month", "type": "Type"},
            color_discrete_map={"income": "#1D9E75", "expense": "#D85A30"}
        )
        fig_bar.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=280,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 2: LINE + GAUGE ──
    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.markdown("""
        <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem;">
            <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:0;">📈 Daily Spending Trend</p>
        """, unsafe_allow_html=True)

        if not df_expense.empty:
            daily = df_expense.groupby("date")["amount"].sum().reset_index()
            fig_line = px.line(
                daily,
                x="date",
                y="amount",
                labels={"amount": "Amount (₹)", "date": "Date"},
                markers=True
            )
            fig_line.update_traces(line_color="#D85A30", marker_color="#D85A30")
            fig_line.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                height=280
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No expense data!")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right2:
        st.markdown("""
        <div style="background:white; border:1px solid #eee; border-radius:12px; padding:1rem 1.25rem;">
            <p style="font-size:13px; font-weight:500; color:#888; margin-bottom:0;">🏦 Savings Rate</p>
        """, unsafe_allow_html=True)

        total_income = df_income["amount"].sum()
        total_expense = df_expense["amount"].sum()

        if total_income > 0:
            savings_rate = ((total_income - total_expense) / total_income) * 100
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(savings_rate, 1),
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [-50, 100]},
                    "bar": {"color": "#1D9E75"},
                    "steps": [
                        {"range": [-50, 20], "color": "#fde8e4"},
                        {"range": [20, 50], "color": "#fef3e2"},
                        {"range": [50, 100], "color": "#e4f5ec"},
                    ]
                }
            ))
            fig_gauge.update_layout(
                margin=dict(t=30, b=10, l=20, r=20),
                height=280
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.info("Add some income to see your savings rate!")

        st.markdown("</div>", unsafe_allow_html=True)