import streamlit as st
import requests
import os

# Streamlit app
st.title("Campaign Data Viewer")

# User authentication
st.header("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    token_url = "https://fastapi-app-kiim.onrender.com"
    form_data = {"username": username, "password": password}
    response = requests.post(token_url, data=form_data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        st.session_state["access_token"] = access_token
        st.success("Login successful!")
    else:
        st.error("Login failed. Please check your credentials.")

# Fetch campaign data
st.header("Fetch Campaign Data")
campaign_id = st.text_input("Campaign ID")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
fetch_button = st.button("Fetch Data")

if fetch_button:
    if "access_token" in st.session_state:
        access_token = st.session_state["access_token"]
        url = "https://fastapi-app-kiim.onrender.com/campaign-data"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            st.json(data)
        else:
            st.error(f"Failed to fetch data: {response.status_code} - {response.text}")
    else:
        st.warning("You need to log in first.")
