import os

master_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_instance_name = os.environ.get("DB_NAME")

endpoint = os.environ.get("DB_HOST")


if __name__ == "__main__":
    print(f"Username: {master_username}")                                                                                    
    print(f"Password: {'********' if db_password else 'Not Set'}")                                                           
    print(f"Endpoint: {endpoint}")                                                                                           
    print(f"DB Name: {db_instance_name}") 