import os
import sys
import json
import pika

EXCHANGE_NAME = "rapido-dispatch"


def get_connection():
    amqp_url = os.getenv("RABBITMQ_URL", "amqp://localhost")
    params = pika.URLParameters(amqp_url)
    return pika.BlockingConnection(params)


def on_message_received(channel, method, properties, body, driver_name):
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:
        print(f"[{driver_name}] Invalid JSON. NACK without requeue. Error: {e}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    # check if required zone field exists
    if "zone" not in data or data["zone"] is None:
        print(f"[{driver_name}] REJECTED: Missing 'zone' in message {data.get('id', 'unknown')}. basic_nack(requeue=False)")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    else:
        req_id = data.get("id")
        city = data.get("city")
        zone = data.get("zone")
        req_type = data.get("type")
        print(f"[{driver_name}] PROCESSED: {req_id} ({city} / {zone} / {req_type}). basic_ack")
        channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    if len(sys.argv) < 3:
        print("Usage: python driver.py <NAME> <BINDING_PATTERN>")
        print("Example: python driver.py Ravi bangalore.koramangala.*")
        sys.exit(1)

    driver_name = sys.argv[1]
    binding_pattern = sys.argv[2]

    connection = get_connection()
    channel = connection.channel()

    # declare topic exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

    # declare exclusive private queue for this driver
    queue_name = f"queue_{driver_name.lower()}"
    channel.queue_declare(queue=queue_name, exclusive=True)

    # bind private queue to exchange with driver's pattern
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=queue_name, routing_key=binding_pattern)

    print(f"[{driver_name}] Connected. Listening on '{binding_pattern}'... (Ctrl+C to stop)")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=lambda ch, method, properties, body: on_message_received(
            ch, method, properties, body, driver_name
        )
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"\n[{driver_name}] Stopping consumer...")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
