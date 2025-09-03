import os
from dotenv import load_dotenv

# Load variables from .env
if not load_dotenv():
    raise FileNotFoundError(".env file is missing! Please create one in the project root.")

# Helper to fetch required env variables
def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise EnvironmentError(f"Missing required environment variable: {key}")
    return value

# Kafka Config
KAFKA_TOPIC = get_env_var("KAFKA_TOPIC")
KAFKA_SERVER = get_env_var("KAFKA_SERVER")

# MongoDB Config
MONGO_URL = get_env_var("MONGO_URL")
MONGO_DATABASE = get_env_var("MONGO_DATABASE")
MONGO_COLLECTION = get_env_var("MONGO_COLLECTION")

# File Paths
LOGIN_FILE = get_env_var("LOGIN_FILE")
CHECKPOINT_FILE = get_env_var("CHECKPOINT_FILE")
