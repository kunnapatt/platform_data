from confluent_kafka import Producer
import time
import cv2

def main() :
    video = cv2.VideoCapture(0)

    bootstrap_servers = "localhost:9092"
    topic = "test-streaming-camera"

    func_producer(
        video, 
        topic=topic,
        bootstrap_servers=bootstrap_servers,
    )

def func_producer(video, topic: str, bootstrap_servers: str) :
    conf = {
        "bootstrap.servers": bootstrap_servers,
    }

    producer = Producer(**conf)

    while video.isOpened() :
        _, frame = video.read()

        if not _ :
            break

        ret, buffer = cv2.imencode(".jpg", frame)
        producer.produce(topic, value=buffer.tobytes())
        time.sleep(0.2)

        producer.poll(0)

    video.release()
    print("Publish success.")
    producer.flush()

if __name__ == "__main__" :
    main()