# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 10000 to allow traffic to the application
EXPOSE 10000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "api.working:app", "--host", "0.0.0.0", "--port", "10000"]
