# Build Instructions
To get the application ready to run, run the following commands:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Create a service for the application
```
sudo nano /etc/systemd/system/WebLayer.service
```

```
[Unit]
Description=Gunicorn instance for a simple hello world app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/WebLayer
ExecStart=/home/ubuntu/WebLayer/.venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
```

Reload the daemon and start the WebLayer service using:
```
sudo systemctl daemon-reload
sudo systemctl start WebLayer
sudo systemctl enable WebLayer
```

# Install NGINX to host the webservice

```sudo apt-get install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

Now we need to edit the default file in the WebLayer directory. Open it and  scroll down to find line 67. Here replace <DNS_of_Internal_ALB> with the DNS of your internal DNS.

Run the following commands to restart the nginx server with the new default file.
```
sudo cp default /etc/nginx/sites-available/default
sudo systemctl restart nginx
```