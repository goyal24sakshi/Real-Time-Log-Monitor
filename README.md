Real-Time Log Monitoring System:

This project implements a real-time log monitoring system using Python, Kafka, and MongoDB.
It captures login events, streams them to Kafka, consumes them for persistence, and provides a live CLI dashboard for monitoring statistics.

Features:
Generate and capture login events.
Real-time event streaming using Apache Kafka.
Event persistence in MongoDB.
CLI dashboard displaying:
Total login attempts
Success and failure counts
Per-user breakdown
Logging for all components.
Checkpointing to prevent duplicate reads.

Running the Project:

1 Start Kafka and MongoDB services.

2 Generate test login events:
python src/main.py

3 Run the producer (monitors file and sends events to Kafka):
python src/login_producer.py

4 Run the consumer (reads from Kafka and writes to MongoDB):
python src/login_consumer.py

5Run the dashboard (displays real-time stats):
python src/dashboard_cli.py

