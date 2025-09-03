import os
import time
from pymongo import MongoClient
from utils.logging_config import logger
from utils.config import MONGO_URL, MONGO_DATABASE, MONGO_COLLECTION


def fetch_stats(collection):
    """
    Fetch aggregate statistics:
    total events, success count, failed count, and per-user breakdown.
    """
    total_events = collection.count_documents({})
    success_count = collection.count_documents({"status": "success"})
    failed_count = collection.count_documents({"status": "failed"})

    # Per-user breakdown
    user_stats = {}
    for doc in collection.find({}):
        userid = doc.get("userid")
        status = doc.get("status")
        if userid not in user_stats:
            user_stats[userid] = {"success": 0, "failed": 0}
        user_stats[userid][status] += 1

    return total_events, success_count, failed_count, user_stats


def display_dashboard(collection):
    """
    Continuously refresh and display login stats in CLI.
    """
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")  # Clear screen
            total, success, failed, user_stats = fetch_stats(collection)

            print("===== LOGIN EVENTS DASHBOARD =====")
            print(f"Total Events: {total}")
            print(f"Success     : {success}")
            print(f"Failed      : {failed}")
            print("\n--- Per User Breakdown ---")
            for user, stats in user_stats.items():
                print(f"{user}: Success={stats['success']}, Failed={stats['failed']}")
            print("==================================")

            logger.info("Dashboard refreshed.")
            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Dashboard stopped by user.")


def main():
    """Connect to MongoDB and start the CLI dashboard."""
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]

    logger.info("Starting CLI dashboard...")
    display_dashboard(collection)

    client.close()


if __name__ == "__main__":
    main()
