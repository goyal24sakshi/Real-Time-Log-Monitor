import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from utils.logging_config import logger
from utils.config import KAFKA_TOPIC, KAFKA_SERVER, MONGO_URL, MONGO_DATABASE, MONGO_COLLECTION


def consume_login_events():
    """
    Consume login events from Kafka and insert them into MongoDB.
    """
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        group_id="login-consumer-group",
        auto_offset_reset="latest",   # process only new messages
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    client = MongoClient(MONGO_URL)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]

    try:
        for message in consumer:
            event = message.value
            logger.info(f"Consumed event: {event}")

            # Insert event into MongoDB
            collection.insert_one(event)
            logger.info("Event inserted into MongoDB.")

    except KeyboardInterrupt:
        logger.info("Consumer stopped manually.")
    finally:
        consumer.close()
        client.close()


if __name__ == "__main__":
    consume_login_events()
