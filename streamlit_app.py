import streamlit as st
import requests
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        numerical_cols = df.select_dtypes(include=['number']).columns
        df_resampled = df[numerical_cols].resample('W').mean()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write("Fetched Campaign Data:")
            st.dataframe(df)

        with col2:
            effectiveness_score = df_resampled["effectiveness"].mean()
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=effectiveness_score,
                gauge={'axis': {'range': [0, 100]}},
                title={'text': "Effectiveness Score"}
            ))
            st.plotly_chart(gauge, use_container_width=True)

        # Display graphs below 
        col1, col2 = st.columns([1, 1])

        with col1:
            if not df_resampled.empty:
                st.subheader("Impressions Over Time")
                fig = px.line(df_resampled, x=df_resampled.index, y="impressions")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if not df_resampled.empty:
                st.subheader("Views Over Time")
                fig = px.line(df_resampled, x=df_resampled.index, y="views")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

# Login page
def login():

    st.markdown(
        """
        <style>
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            text-align: center;
        }
        .login-title {
            font-size: 30px;
            color: #efbf4a;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        token = get_token(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful")
            st.session_state.page = "campaign_data"
        else:
            st.error("Login failed")

# Main function for the Streamlit app
def main():
    st.set_page_config(layout='wide')

    # Custom CSS for header 
    st.markdown(
        """
        <style>
        .title {
            font-size: 30px;
            margin-bottom: 1rem;
            color: #efbf4a;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "token" not in st.session_state:
        login()
    else:
        st.markdown('<div class="title">Campaign Data Viewer</div>', unsafe_allow_html=True)

        st.markdown('<div class="container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            campaign_id = st.text_input("Campaign ID")
        with col2:
            start_date = st.date_input("Start Date", datetime.date.today())
        with col3:
            end_date = st.date_input("End Date", datetime.date.today())

        if st.button("Fetch Data"):
            st.session_state.campaign_data = fetch_campaign_data(start_date, end_date, campaign_id)

        st.markdown('</div>', unsafe_allow_html=True)

        if "campaign_data" in st.session_state:
            show_campaign_data()

# Run the app
if __name__ == "__main__":
    main()
