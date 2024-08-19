import streamlit as st
import requests
from datetime import date

FASTAPI_URL = "https://fastapi-app-kiim.onrender.com"

st.title("Campaign Data Viewer")

# User login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post(
        "https://fastapi-app-kiim.onrender.com/token",
        data={"username": username, "password": password},
    )
    if response.status_code == 200:
        token = response.json().get("access_token")
        st.session_state["token"] = token
        st.success("Logged in successfully!")
    else:
        st.error("Login failed: Check your username and password.")

# Token-based request
if "token" in st.session_state:
    st.write("You are logged in as:", username)
    campaign_id = st.text_input("Campaign ID (optional)")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date", value=date.today())

    if st.button("Get Campaign Data"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        params = {
            "campaign_id": campaign_id,
            "start_date": start_date,
            "end_date": end_date,
        }
        
        # Ensure that date range is valid
        if start_date > end_date:
            st.error("Start date cannot be after end date.")
        else:
            response = requests.get(
                "https://fastapi-app-kiim.onrender.com/campaign-data", headers=headers, params=params
            )
            if response.status_code == 200:
                data = response.json()
                st.write("Campaign Data:")
                st.json(data)
            elif response.status_code == 401:
                st.error("Unauthorized: Please log in again.")
            else:
                st.error(f"Failed to retrieve data: {response.status_code} - {response.text}")
else:
    st.info("Please log in to access campaign data.")
