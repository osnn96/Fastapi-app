import streamlit as st
import requests
from datetime import datetime

st.title("Campaign Data Viewer")

# Section for Login
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    # Get the token
    token_url = "http://localhost:10000/token"
    form_data = {
        "username": username,
        "password": password
    }
    response = requests.post(token_url, data=form_data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        st.session_state["access_token"] = access_token
        st.success("Login successful!")
    else:
        st.error("Login failed. Please check your credentials.")

# Use the token to access the API
if "access_token" in st.session_state:
    st.subheader("Fetch Campaign Data")
    campaign_id = st.text_input("Campaign ID")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Fetch Data"):
        url = "http://localhost:10000/campaign-data"  
        params = {
            "campaign_id": campaign_id,
            "start_date": start_date.strftime('%Y-%m-%d') if start_date else None,  # Format the date
            "end_date": end_date.strftime('%Y-%m-%d') if end_date else None  # Format the date
        }
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            st.write("Campaign Data:", data)
        else:
            st.error(f"Failed to fetch data: {response.status_code} - {response.text}")
