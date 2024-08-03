from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
import cv2
import sys
import os
import uuid
from flask import Flask, Response

app = Flask(__name__)

def main() :

    app.run(host="0.0.0.0", port=3333, debug=True)

@app.route('/test-video', methods=["GET"])
def test_get_video() :
    bootstrap_server = "localhost:9092"
    topic = "test-streaming-video"
    return Response(
        consumer(topic=topic, bootstrap_server=bootstrap_server),
        mimetype=f"multipart/x-mixed-replace; boundary=frame"
    )

def consumer(topic: str, bootstrap_server: str) :

    conf = {
        "bootstrap.servers": bootstrap_server,
        "group.id": uuid.uuid1(),
        "session.timeout.ms": 6000,
        "default.topic.config": {
            # "auto.offset.reset": "earliest"
            "auto.offset.reset": "latest"
        }
    }
    
    cons = Consumer(**conf)
    try :
        cons.subscribe([topic])

        while True :
            msg = cons.poll(timeout=10.0)
            if msg is None: continue

            if msg.error() :
                if msg.error().code == KafkaError._PARTITION_EOF :
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))

                elif msg.error() :
                    raise KafkaException(msg.error())
            else :
                print(msg)
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpg\r\n\r\n" + msg.value() + b"\r\n\r\n"
                )
                # print(msg.value())             

    finally :
        cons.close()
    

if __name__ == "__main__" :
    main()