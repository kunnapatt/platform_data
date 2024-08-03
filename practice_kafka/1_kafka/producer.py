from confluent_kafka import Producer
import time

def main() :
    msg_count = int(1e6)
    msg_size = 10
    msg_payload = ("kafkatest" * 2).encode()[:msg_size] ### message send

    bootstrap_servers = 'localhost:9092'
    topic = "test2"

    producer_performance(
        topic=topic, 
        bootstrap_servers=bootstrap_servers, 
        msg_count=msg_count, 
        msg_payload=msg_payload
    )

def calculate_thoughput(timing, n_messages=1000000, msg_size=100):
    ##### Calculate thoughput of data
    print("Processed {0} messsages in {1:.2f} seconds".format(n_messages, timing))
    print("{0:.2f} MB/s".format((msg_size * n_messages) / timing / (1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages / timing))

def producer_performance(
    topic: str, 
    bootstrap_servers: str, 
    msg_count: int, 
    msg_payload
) :
    conf = {
        "bootstrap.servers": bootstrap_servers,
    }

    producer = Producer(**conf)
    msg_to_retry = []
    producer_start = time.time()

    for _ in range(msg_count) :
        try :
            ###### Publish message to topic on zookeeper
            producer.produce(topic, value=msg_payload)
        except BufferError as e :
            msg_to_retry.append(msg_payload)

    for msg in msg_to_retry :
        producer.poll(0)
        try :
            producer.produce(topic, value=msg)
        except BufferError as e :
            producer.poll(0)
            producer.produce(topic, value=msg)

    producer.flush()
    return time.time() - producer_start


if __name__ == "__main__" :
    main()