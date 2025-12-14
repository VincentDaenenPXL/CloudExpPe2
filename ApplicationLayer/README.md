# API Documentation

## Introduction

Brief introduction to the Application Layer.


## Endpoints

### `GET /`

Get a list of todo tasks.

#### Parameters

- None

#### Response

```json
[
  {
    "id": "task-1"
  },
  {
    "1": "Get Milk"
  }
]
```
### `GET /health`

Get status code 200 with a message.

#### Parameters

- None

#### Response

```json
{
  "status_code": 200,
  "message": "Successful health check for ALB!"
}
```

### `POST /create`

Create a new todo task.

#### Headers
- Content-Type: `application/x-www-form-urlencoded`

#### Request Body
The request body should be URL-encoded and contain the following form parameters:

- **task** (string, required): The name of the todo task.

#### Response

```json
{
    "message": "Form submitted successfully!"
}

{
    "error": "Invalid form data. Please provide valid values for name, email, and message."
}
```

### `POST /update`

Update an existing todo task.

#### Headers
- Content-Type: `application/x-www-form-urlencoded`

#### Request Body
The request body should be URL-encoded and contain the following form parameters:

- **task_id** (string, required): The id of the todo task to update.
- **task** (string, required): The new name of the todo task.

#### Response

```json
{
    "message": "Form submitted successfully!"
}

{
    "error": "Invalid form data. Please provide valid values for name, email, and message."
}
```

### `POST /complete/<task_id>`

Complete an existing todo task.

- **task_id** (integer, required):  The id of the todo task to complete.

### Response

#### Status Codes
- 302 OK: User information retrieved successfully.
- 404 Not Found: User not found.

# Build Instructions

## Database
make sure the an RDS Database is created for this with the following DBinit before youset up this applicationLayer.

```
CREATE DATABASE webappdb;
SHOW DATABASES;
USE webappdb;

CREATE TABLE IF NOT EXISTS todotable(id INT NOT NULL AUTO_INCREMENT, task VARCHAR(100), PRIMARY KEY(id));

SHOW TABLES;

INSERT INTO todotable (task) VALUES ('Aan CloudPE werken');

SELECT * FROM todotable;
```

## Application Layer Application

Make sure to install the dependencies and PM2 to allow automated startup (as a daemon)
```
pip3 install -r requirements.txt
export PATH="/home/ec2-user/.local/bin:$PATH"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
source ~/.bashrc
nvm install 16
nvm use 16
npm install -g pm2
```

Link the startup of the application with the python3 interpreter
```
pm2 start app.py --interpreter python3
```
Make sure the localhost keeps on running even after the server is interrupted do the following:

```
pm2 startup
```

Running thi will give an output prompting you to asdd a new $PATH. Do what is said.