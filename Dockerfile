# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports for both FastAPI and Streamlit
EXPOSE 10000
EXPOSE 8501

# Command to run FastAPI and Streamlit
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port 8501 & uvicorn api.working:app --host 0.0.0.0 --port 10000"]
