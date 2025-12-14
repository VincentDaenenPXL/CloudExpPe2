# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Command to run the application
# The database connection parameters are retrieved from AWS SSM Parameter Store via parameters.py
CMD ["python", "app.py"]
