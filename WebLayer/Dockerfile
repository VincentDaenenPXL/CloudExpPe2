# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Step 2: Install Nginx
RUN echo "deb http://archive.debian.org/debian/ buster main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y nginx curl

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy application code and necessary scripts
COPY . .

# Step 6: Copy the Nginx configuration file
COPY default /etc/nginx/sites-available/default

# Step 7: Copy and set permissions for the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Step 8: Expose port 80 for Nginx
EXPOSE 80

# Step 9: Use the entrypoint script to start services
ENTRYPOINT ["/entrypoint.sh"]

