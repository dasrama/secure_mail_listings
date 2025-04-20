import streamlit as st
import requests
from urllib.parse import parse_qs

API_BASE_URL = "http://localhost:8000"

st.title("Secure Email Listing")
query_params = st.query_params

token = query_params.get("token", None)
email = query_params.get("email", None)

if email and "email" not in st.session_state:
    st.session_state["email"] = email
    st.success(f" Welcome, {email}!")

st.sidebar.header("Login with Gmail")
if st.sidebar.button("Login with Gmail"):
    st.markdown(
        f"[🔗 Click to Sign in with Google](http://localhost:8000/auth/login)",
        unsafe_allow_html=True
    )

if token:
    st.session_state["token"] = token
    st.header("Your Emails")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_BASE_URL}/emails/", headers=headers)

    if response.status_code == 200:
        emails = response.json()
        for email in emails:
            with st.expander(f"📧 {email['subject']}"):
                st.write(f"**From:** {email['email_address']}")
                st.write(f"**Time:** {email['timestamp']}")
                if email.get("documents"):
                    for doc in email["documents"]:
                        st.markdown(f"[Download]({doc})")
                else:
                    st.write("No attachments.")
    else:
        st.error("Failed to fetch emails.")
else:
    st.warning("Please login to view your emails.")
