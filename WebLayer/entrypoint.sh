#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Start the Gunicorn web server in the background.
# It listens on 127.0.0.1:8000, which is where Nginx will proxy requests to.
gunicorn -w 4 -b 127.0.0.1:8000 app:app &

# Use envsubst to replace environment variables in the Nginx config template.
envsubst '$INTERNAL_ALB_DNS_NAME' < /etc/nginx/sites-available/default > /etc/nginx/sites-available/default.tmp

# Replace the original config file with the processed one.
mv /etc/nginx/sites-available/default.tmp /etc/nginx/sites-available/default

# Start Nginx in the foreground. 'exec' replaces the shell process with nginx,
# which is standard practice for the main process in a container.
exec nginx -g 'daemon off;'
