import streamlit as st
from db.database import create_tables
from utils.auth import login_user, signup_user

st.set_page_config(
    page_title="VaultView",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f0f2f6;
        padding: 4px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-size: 14px;
        font-weight: 400;
        color: #666;
        background: transparent;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1D9E75 !important;
        font-weight: 500;
        border: 1px solid #e0e0e0 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }
    [data-testid="metric-container"] {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #eee;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        border: 1px solid #e0e0e0;
    }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
    }
    hr { border-color: #eee; }
</style>
""", unsafe_allow_html=True)

create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = ""

# ─────────────────────────────────────────
# 🔐 AUTH PAGE
# ─────────────────────────────────────────
def show_auth_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:2rem 0 1.5rem 0;">
            <div style="display:inline-flex; align-items:center; justify-content:center;
                        width:56px; height:56px; background:#1D9E75; border-radius:14px;
                        margin-bottom:12px;">
                <span style="font-size:28px;">💰</span>
            </div>
            <h1 style="font-size:26px; font-weight:600; color:#1a1a1a; margin:0;">VaultView</h1>
            <p style="color:#888; font-size:14px; margin-top:4px;">Your personal finance tracker</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            username = st.text_input("Username", key="login_user", placeholder="Enter your username")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Login →", use_container_width=True, key="login_btn"):
                if username and password:
                    success, user_id, message = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields!")

        with tab2:
            new_username = st.text_input("Choose a Username", key="signup_user", placeholder="Pick a username")
            new_password = st.text_input("Choose a Password", type="password", key="signup_pass", placeholder="Min. 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_pass", placeholder="Repeat your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account →", use_container_width=True, key="signup_btn"):
                if new_username and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords don't match!")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters!")
                    else:
                        success, message = signup_user(new_username, new_password)
                        if success:
                            st.success(message + " Please log in!")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill in all fields!")

# ─────────────────────────────────────────
# 🏠 MAIN APP
# ─────────────────────────────────────────
def show_main_app():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; padding-bottom:0.5rem;">
            <div style="width:38px; height:38px; background:#1D9E75; border-radius:10px;
                        display:flex; align-items:center; justify-content:center; font-size:20px;">
                💰
            </div>
            <div>
                <span style="font-size:20px; font-weight:600; color:#1a1a1a;">VaultView</span>
                <span style="font-size:13px; color:#888; margin-left:8px;">Personal Finance Tracker</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        inner1, inner2 = st.columns([2, 1])
        with inner1:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; padding-top:0.4rem; justify-content:flex-end;">
                <div style="width:30px; height:30px; background:#E1F5EE; border-radius:50%;
                            display:flex; align-items:center; justify-content:center;
                            font-size:12px; font-weight:500; color:#0F6E56;">
                    {st.session_state.username[:2].upper()}
                </div>
                <span style="font-size:13px; color:#666;">{st.session_state.username}</span>
            </div>
            """, unsafe_allow_html=True)
        with inner2:
            if st.button("Logout", key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.user_id = None
                st.session_state.username = ""
                st.rerun()

    st.markdown("<hr style='margin:0 0 1rem 0;'>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠  Dashboard",
        "💸  Transactions",
        "📊  Reports",
        "📋  History"
    ])

    with tab1:
        from views.dashboard import show_dashboard
        show_dashboard()

    with tab2:
        from views.transactions import show_transactions
        show_transactions()

    with tab3:
        from views.reports import show_reports
        show_reports()

    with tab4:
        from views.history import show_history
        show_history()

# ─────────────────────────────────────────
# 🚦 ENTRY POINT
# ─────────────────────────────────────────
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_page()