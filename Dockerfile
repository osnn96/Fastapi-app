# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add the startup script to the container
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose ports for both FastAPI and Streamlit
EXPOSE 10000 8501

# Command to run both FastAPI and Streamlit using the startup script
CMD ["/app/start.sh"]
