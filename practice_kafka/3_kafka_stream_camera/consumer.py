from confluent_kafka import Consumer, KafkaError, KafkaException
import cv2
import sys
import os
import uuid
from flask import Flask, Response

app = Flask(__name__)

def main() :
    app.run(host="0.0.0.0", port=3333, debug=False)


@app.route("/test-camera", methods=["GET"])
def test_get_camera() :
    bootstrap_server = "localhost:9092"
    topic = "test-streaming-camera"

    return Response(
        func_consumer(topic=topic, bootstrap_servers=bootstrap_server),
        mimetype=f"multipart/x-mixed-replace; boundary=frame"
    )
    pass

def func_consumer(topic: str, bootstrap_servers: str) :

    conf = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": uuid.uuid1(),
        "session.timeout.ms": 6000,
        "default.topic.config": {
            "auto.offset.reset": "latest",
        }
    }

    consumer = Consumer(**conf)

    try :
        consumer.subscribe([topic])

        while True :
            msg = consumer.poll(timeout=10.0)
            if not msg :
                continue
            if msg.error() :
                if msg.error().code == KafkaError._PARTITION_EOF :
                    sys.stderr.write(
                        '%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset())
                    )

                elif msg.error() :
                    raise KafkaException(msg.error())
            else :
                # print(msg)
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpg\r\n\r\n" + msg.value() + b"\r\n\r\n"
                )
    finally :
        consumer.close()

if __name__ == "__main__" :
    main()