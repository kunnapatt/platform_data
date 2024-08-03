from confluent_kafka import Consumer, KafkaError, KafkaException
import uuid
import time
import sys

def main() :
    bootstrap_server = "localhost:9092"
    msg_count = int(1e6)
    topic = "test"
    consumer_timing = {}
    pass

def calculate_thoughput(timing, n_messages=1000000, msg_size=100):
    print("Processed {0} messsages in {1:.2f} seconds".format(n_messages, timing))
    print("{0:.2f} MB/s".format((msg_size * n_messages) / timing / (1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages / timing))

def consumer_performance(topic: str, bootstrap_server: str) :
    pass
    conf = {
        "bootstrap.servers": bootstrap_server,
        "group.id": uuid.uuid1(),
        "session.timeout.ms": 6000,
        "default.topic.config": {
            "auto.offset.reset": "earliest"
        }
    }

    consumer = Consumer(**conf)
    basic_consume_loop(
        consumer=consumer,
        topics=[topic],
    )

def basic_consume_loop(consumer, topics: list) :
    try :
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(timeout=1.0) ##### delay (1ms)
            if msg is None: continue

            if msg.error() :
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))

                elif msg.error() :
                    raise KafkaException(msg.error())
            else :
                print(msg.value())
    finally :
        consumer.close()

if __name__ == "__main__" :
    main()