import streamlit as st
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Function to get the authentication token
def get_token(username, password):
    response = requests.post(
        "http://fastapi:8000/token",
        data={"username": username, "password": password},
    )
    return response.json().get("access_token")

# Function to fetch campaign data based on the given parameters
def fetch_campaign_data(start_date, end_date, campaign_id):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(
        f"http://fastapi:8000/campaign-data?start_date={start_date}&end_date={end_date}&campaign_id={campaign_id}",
        headers=headers,
    )
    return response.json()

# Show campaign data with visualization
def show_campaign_data():
    data = st.session_state.campaign_data
    
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Display the DataFrame
    st.write("Fetched Campaign Data:")
    st.dataframe(df)
    
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])  # Ensure 'date' is in datetime format
        df.set_index("date", inplace=True)

        # Select only numerical columns for resampling
        numerical_cols = df.select_dtypes(include=['number']).columns
        df_resampled = df[numerical_cols].resample('W').mean()

        # Apply a style
        plt.style.use('seaborn-darkgrid')

        # Plotting
        if not df_resampled.empty:
            # Impressions Over Time
            st.write("Impressions Over Time:")
            fig, ax = plt.subplots(figsize=(12, 6))
            df_resampled["impressions"].plot(ax=ax, label="Impressions", color='blue', linewidth=2)
            ax.set_title("Impressions Over Time", fontsize=16)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Impressions", fontsize=12)
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Views Over Time
            st.write("Views Over Time:")
            fig, ax = plt.subplots(figsize=(12, 6))
            df_resampled["views"].plot(ax=ax, label="Views", color='green', linewidth=2)
            ax.set_title("Views Over Time", fontsize=16)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Views", fontsize=12)
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

            # Effectiveness Over Time
            st.write("Effectiveness Over Time:")
            fig, ax = plt.subplots(figsize=(12, 6))
            df_resampled["effectiveness"].plot(ax=ax, label="Effectiveness", color='red', linewidth=2)
            ax.set_title("Effectiveness Over Time", fontsize=16)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Effectiveness", fontsize=12)
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

# Login page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        token = get_token(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful")
            
            # Redirect to the campaign data page
            st.session_state.page = "campaign_data"
        else:
            st.error("Login failed")

# Main function for the Streamlit app
def main():
    if "token" not in st.session_state:
        login()
    else:
        st.title("Campaign Data")
        
        # Date selectors for start date and end date
        start_date = st.date_input("Start Date", datetime.date.today())
        end_date = st.date_input("End Date", datetime.date.today())
        
        campaign_id = st.text_input("Campaign ID")
        
        if st.button("Fetch Data"):
            st.session_state.campaign_data = fetch_campaign_data(start_date, end_date, campaign_id)
        
        if "campaign_data" in st.session_state:
            show_campaign_data()

# Run the app
if __name__ == "__main__":
    main()