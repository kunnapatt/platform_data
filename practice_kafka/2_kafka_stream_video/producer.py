from confluent_kafka import Producer
import cv2
import os

def main() :
    directory = os.path.dirname(os.path.realpath(__file__))

    path = os.path.join(directory, "IMG_5755.MOV")
    video = cv2.VideoCapture(path)

    bootstrap_servers = 'localhost:9092'
    topic = "test-streaming-video"

    producer(video, topic=topic, bootstrap_servers=bootstrap_servers)

def producer(
    video,
    topic: str,
    bootstrap_servers: str, 
    
) :

    conf = {
        "bootstrap.servers": bootstrap_servers,
    }

    prod = Producer(**conf)

    while video.isOpened() :
        _, frame = video.read()

        if not _ :
            break

        ret, buffer = cv2.imencode(".jpg", frame)
        prod.produce(topic, value=buffer.tobytes())
        prod.poll(0)
    video.release()
    print("Publish success.")
    prod.flush()


if __name__ == "__main__" :
    main()