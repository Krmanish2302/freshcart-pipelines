import os
import sys
import time
import json
import random
import pika

EXCHANGE_NAME = "rapido-dispatch"
CITIES = ["bangalore", "chennai"]
ZONES = ["koramangala", "indiranagar", "whitefield", "tnagar"]
TYPES = ["ride", "food"]


def get_connection():
    amqp_url = os.getenv("RABBITMQ_URL", "amqp://localhost")
    params = pika.URLParameters(amqp_url)
    return pika.BlockingConnection(params)


def main():
    connection = get_connection()
    channel = connection.channel()

    # declare topic exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

    order_counter = 1
    print(f"[*] Dispatcher started. Publishing to exchange '{EXCHANGE_NAME}'...")

    try:
        while True:
            city = random.choice(CITIES)
            zone = random.choice(ZONES)
            req_type = random.choice(TYPES)

            # routing key: city.zone.type
            routing_key = f"{city}.{zone}.{req_type}"

            # 1 in 10 messages simulates a malformed request missing the zone field
            is_bad_message = (order_counter % 10 == 0)
            if is_bad_message:
                payload = {
                    "id": f"REQ-{order_counter:04d}",
                    "city": city,
                    "type": req_type,
                    "ts": time.time()
                }
            else:
                payload = {
                    "id": f"REQ-{order_counter:04d}",
                    "city": city,
                    "zone": zone,
                    "type": req_type,
                    "ts": time.time()
                }

            message_body = json.dumps(payload)
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json"
                )
            )

            status = "MALFORMED (missing zone)" if is_bad_message else "OK"
            print(f"[x] Sent [{routing_key}] ({status}): {message_body}")

            order_counter += 1
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopping dispatcher...")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
