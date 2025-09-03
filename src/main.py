from datetime import datetime
import json
from utils.logging_config import logger
from utils.config import LOGIN_FILE


def main():
    """
    CLI to capture login events (userid + status) 
    and append them to a JSON file with timestamp.
    """
    logger.info("Application started.")

    while True:
        # Take user input
        userid = input("Enter userid (or type 'exit' to stop): ").strip()
        if userid.lower() == "exit":
            break

        status = input("Enter status (success/failed): ").strip().lower()

        # Validate input
        if not userid or status not in ["success", "failed"]:
            logger.warning("Invalid details entered.")
            continue

        # Create login event with timestamp
        event = {
            "userid": userid,
            "status": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        logger.info(f"Storing login event: {event}")

        # Append event to file
        with open(LOGIN_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")

    logger.info("Exiting main input loop.")


if __name__ == "__main__":
    main()
