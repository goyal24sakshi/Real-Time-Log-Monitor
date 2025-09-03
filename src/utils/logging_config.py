import logging

logger = logging.getLogger()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs\logs.log"),   # logs to file
        logging.StreamHandler()            # logs to console
    ]
)