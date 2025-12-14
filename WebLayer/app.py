from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import urllib.request, json
import requests
import os

app = Flask(__name__)

# Get the backend API URL from environment variable, with a fallback for local dev
backend_api_url = os.getenv('BACKEND_API_URL', 'http://127.0.0.1:4000')


@app.route('/')
def index():
    todos={}

    try:
        # The backend endpoint for getting all todos is the root '/'
        url = backend_api_url
        response = requests.get(url, timeout=5)
        todos = json.loads(response.content)
    except Exception as ex:
        # Log the exception for debugging purposes
        print(f"Could not connect to backend API at {url}: {ex}")

    return render_template('index.html', todos=todos)

if __name__ == "__main__":
    app.run()