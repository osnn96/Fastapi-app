# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by the `PORT` environment variable
EXPOSE 8501  
# Match the port Streamlit uses

# Command to run both FastAPI and Streamlit on the same port
CMD ["sh", "-c", "uvicorn api.working:app --host 0.0.0.0 --port $PORT & streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"]

