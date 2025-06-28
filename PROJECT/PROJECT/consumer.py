# consumer.py

import pika
import json
from log_manager import setup_logger
from main import run_automation_from_dict

def callback(ch, method, properties, body):
    logger = setup_logger()
    logger.info("Received a new message from the queue")

    try:
        data = json.loads(body.decode("utf-8"))

        if isinstance(data, list):
            logger.info(f"Message contains {len(data)} applications")
            for i, cred in enumerate(data):
                logger.info(f"Processing application {i + 1} for {cred.get('username', 'unknown')}")
                run_automation_from_dict(cred, logger)
        else:
            logger.info("Processing single application")
            run_automation_from_dict(data, logger)

    except Exception as e:
        logger.error(f"Failed to process application(s): {e}")

    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("Message acknowledged")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'visa_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(f"[*] Waiting for messages in '{queue_name}'. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
