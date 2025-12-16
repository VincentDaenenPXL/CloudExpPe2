from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import urllib.request, json
import requests
import os

app = Flask(__name__)


@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/')
def index():
    todos={}

    try:
        url = os.environ.get("INTERNAL_ALB_DNS_NAME", "http://localhost/api/")
        response = requests.get(url, timeout=60)
        todos = json.loads(response.content)
    except Exception as ex:
        exc = str(ex)

    return render_template('index.html', todos=todos)

if __name__ == "__main__":
    app.run()