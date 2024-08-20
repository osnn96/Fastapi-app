import streamlit as st
import requests
import matplotlib.pyplot as plt

def get_token(username, password):
    try:
        response = requests.post(
            "http://fastapi:8000/token", 
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
    except requests.RequestException as e:
        st.error(f"Error connecting to FastAPI: {e}")
    return None

def show_campaign_data():
    st.title("Campaign Data")
    #date burda değişilecek şimdilik bırakıldı
    date = st.date_input("Select Date")
    campaign_id = st.text_input("Campaign ID")
    
    if st.button("Fetch Data"):
        try:
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.get(
                f"http://fastapi:8000/campaign-data?date={date}&campaign_id={campaign_id}",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                # Example plot
                fig, ax = plt.subplots()
                ax.plot(data['x'], data['y'])
                st.pyplot(fig)
            else:
                st.error("Failed to fetch data")
        except requests.RequestException as e:
            st.error(f"Error fetching data: {e}")

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token = get_token(username, password)
        if token:
            st.session_state.token = token
            st.session_state.logged_in = True
            st.session_state.page = "campaign_data"  # Set page to redirect
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

def main():
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        if 'page' in st.session_state and st.session_state.page == "campaign_data":
            show_campaign_data()
        else:
            st.warning("Redirecting to the campaign data page...")
            st.session_state.page = "campaign_data"  # Ensure page is set
            st.experimental_rerun()  # Force a re-run to update the page content
    else:
        login()

if __name__ == "__main__":
    main()
