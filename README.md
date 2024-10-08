# FastAPI Application with Authentication, Database Integration, and Streamlit Interface

This repository contains a FastAPI application with user authentication using OAuth2, environment variable management with `python-dotenv`, integration with a MySQL database, and a Streamlit interface for data visualization. The application includes endpoints for authentication and fetching campaign data, with the configuration loaded from a `.env` file.

## Features

- **User Authentication**: Secure login with JWT tokens.
- **Database Integration**: Connects to a MySQL database and fetches campaign data.
- **Streamlit Interface**: Provides a web-based interface for visualizing campaign data.
- **Environment Variables**: Uses `.env` file for configuration.
- **Docker Support**: Includes Docker setup for containerization.

## Prerequisites

- Python 3.9 or later
- Docker and Docker Compose (for containerization)

## Setup

### 1. Clone the Repository

    git clone https://github.com/osnn96/Fastapi-app.git
    cd Fastapi-app

### 2. Create and Configure the .env File
Create a .env file in the root directory of the project with the following content. Replace the placeholders with your actual values:

SECRET_KEY="your_generated_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
DATABASE_URL="mysql+pymysql://your_user:your_password@your_host/your_database"

    SECRET_KEY: A strong, randomly generated key for signing JWT tokens. To generate a new secret key, use the following commands:
    
    pip install openssl
    openssl rand -base64 32

    DATABASE_URL: Your MySQL database connection string.

### 3. Install Dependencies
Install the required Python packages:

    pip install -r requirements.txt

### 4. Run the Application Locally
You can run the FastAPI application locally using Uvicorn:

    uvicorn api.working:app --reload

To access the Streamlit interface, use:

    streamlit run streamlit_app.py

### 5.. Run with Docker
To build and run the application using Docker, use the following commands:

    docker-compose up --build

This will build the Docker image and start both the FastAPI and Streamlit applications in a containerized environment.

Endpoints
-Authentication
    POST /token: Obtain a JWT token for authentication.

        Request Body:

            {
              "username": "your_username",
              "password": "your_password"
            }
            Response:
            
            {
              "access_token": "your_access_token",
              "token_type": "bearer"
            }

-Campaign Data
    GET /campaign-data: Fetch campaign data with optional query parameters for filtering.
        Query Parameters:
        campaign_id: (Optional) Filter by campaign ID.
        start_date: (Optional) Start date for the data range.
        end_date: (Optional) End date for the data range.

        Response:
        [
          {
            "campaign_id": "123",
            "campaign_name": "Campaign Name",
            "date": "2024-01-01",
            "views": 1000,
            "impressions": 1500,
            "cpm": 5,
            "clicks": 100,
            "media": 75,
            "creative": 80,
            "effectiveness": 90
          }
        ]

Notes

-Make sure to use the correct database credentials and secret key.

-If you encounter issues, check the logs for errors and ensure all environment variables are correctly set.

Contributing

Feel free to contribute to this project by submitting issues or pull requests. For any questions or feedback, open an issue in this repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


This README.md provides clear instructions for setting up, running, and using your FastAPI application. It includes steps for both local development and Docker-based deployment, as well as details about the API endpoints and configuration.


