# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY ./api /app/api
COPY streamlit_app.py /app/

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Command to run both FastAPI and Streamlit applications
CMD ["sh", "-c", "uvicorn api.working:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501"]
