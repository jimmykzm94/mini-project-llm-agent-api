# Use the official Python image from the Docker Hub
FROM python:3.12.8-alpine

# Update system packages and clean up the cache to keep the image small
# Combining update and upgrade in one RUN command creates a single layer.
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# We use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Make port 6001 and 6002 available to the world outside this container
EXPOSE 6001 6002

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run start_server.py when the container launches
CMD ["python", "start_server.py"]