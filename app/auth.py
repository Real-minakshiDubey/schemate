"""
Authentication View for Schemate AI.
Provides responsive, dark-themed login and account creation interfaces
with validation and smooth tab switching.
"""

import streamlit as st
from app.db import register_user, authenticate_user


def render_auth_view():
    """
    Renders login and signup screens with form validation and modern styling.
    Responsive across mobile, desktop, and split-screen developer layouts.
    """
    # Responsive centered column layout
    _, col_center, _ = st.columns([0.1, 0.8, 0.1])

    with col_center:
        st.markdown("## 🏛️ Schemate AI")
        st.caption("AI Assistant for Indian Government Schemes")
        st.markdown("")

        tab_login, tab_signup = st.tabs(["🔑  Sign In", "✨  Create Account"])

        with tab_login:
            _render_login_form()

        with tab_signup:
            _render_signup_form()


def _render_login_form():
    """Renders the login form with validation."""
    with st.form("login_form", clear_on_submit=False):
        st.markdown("#### Welcome Back")
        email = st.text_input("Email Address", placeholder="name@example.com", key="login_email_input")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pw_input")

        submit = st.form_submit_button("Sign In to Schemate", use_container_width=True)

        if submit:
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                success, message, user = authenticate_user(email, password)
                if success and user:
                    st.session_state.user = user
                    st.session_state.messages = []
                    st.session_state.current_conversation_id = None
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


def _render_signup_form():
    """Renders the account creation form with validation."""
    with st.form("signup_form", clear_on_submit=False):
        st.markdown("#### Create your Account")
        name = st.text_input("Full Name", placeholder="Rahul Sharma", key="signup_name_input")
        email = st.text_input("Email Address", placeholder="rahul@example.com", key="signup_email_input")
        password = st.text_input("Password", type="password", placeholder="At least 6 characters", key="signup_pw_input")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", key="signup_cpw_input")

        submit = st.form_submit_button("Create Schemate Account", use_container_width=True)

        if submit:
            if not name.strip():
                st.error("Please provide your full name.")
            elif not email.strip():
                st.error("Please enter a valid email address.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please verify and try again.")
            else:
                success, message, user = register_user(email, name, password)
                if success and user:
                    st.session_state.user = user
                    st.session_state.messages = []
                    st.session_state.current_conversation_id = None
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
