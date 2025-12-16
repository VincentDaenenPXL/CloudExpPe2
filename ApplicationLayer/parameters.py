import os

env = os.environ.get("ENVIRONMENT", "Test")

master_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
endpoint = os.environ.get("DB_ENDPOINT")
db_instance_name = os.environ.get("DB_NAME")

if __name__ == "__main__":
    print(master_username, db_password, endpoint, db_instance_name)