import json
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaProducer
from utils.logging_config import logger
from utils.config import KAFKA_TOPIC, KAFKA_SERVER, LOGIN_FILE, CHECKPOINT_FILE


# Kafka Producer instance
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


class LoginFileHandler(FileSystemEventHandler):
    """
    Watches the login events file for changes and 
    sends new lines as events to Kafka.
    """
    def __init__(self):
        super().__init__()
        self.last_position = self.load_checkpoint()

    def load_checkpoint(self):
        """Return last read byte position from checkpoint file"""
        if os.path.exists(CHECKPOINT_FILE):
            with open(CHECKPOINT_FILE, "r") as f:
                try:
                    return int(f.read().strip())
                except ValueError:
                    return 0
        return 0

    def save_checkpoint(self, position):
        """Save current byte position to checkpoint file"""
        with open(CHECKPOINT_FILE, "w") as f:
            f.write(str(position))

    def on_modified(self, event):
        """Triggered when login file is modified"""
        if event.src_path.endswith(LOGIN_FILE):
            logger.info("Detected file change. Reading new events...")

            with open(LOGIN_FILE, "r") as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()

            # Save checkpoint
            self.save_checkpoint(self.last_position)

            # Send each new line to Kafka
            for line in new_lines:
                try:
                    event_data = json.loads(line.strip())
                    producer.send(KAFKA_TOPIC, event_data)
                    logger.info(f"Produced event: {event_data}")
                except Exception as e:
                    logger.error(f"Error producing event: {e}")


def watch_file():
    """Start monitoring the login events file"""
    event_handler = LoginFileHandler()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=False)
    observer.start()
    logger.info("Producer started watching file for changes...")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_file()
