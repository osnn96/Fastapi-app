# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install supervisor

# Expose the port used by Render
EXPOSE 8501

# Copy the supervisor configuration file
COPY supervisord.conf /etc/supervisor/supervisord.conf

# Command to run supervisor
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
