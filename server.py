import paho.mqtt.client as mqtt
import json
from topic_detection import extract_topic
from const import BROKERS, TOPICS

class MQTTServer:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Server connected to MQTT broker (RC: {rc})")
        for topik in ["kesehatan", "politik", "pendidikan"]:
            client.subscribe(f"chat/messages/{topik}")
            print(f"Subscribed to chat/messages/{topik}")

    def on_message(self, client, userdata, msg):
        print(f"Pesan diterima: {msg.topic} - {msg.payload.decode()}")
        try:
            data = json.loads(msg.payload.decode())
            sender = data["sender"]
            message = data["message"]

            topic_name = msg.topic.split("/")[-1]
            topics = [topic_name]

            topic_channel = f"topic/{topic_name}"
            client.publish(topic_channel, json.dumps({
                "sender": sender,
                "message": message,
                "topics": topics,
                "processed": True
            }))
            print(f"Pesan diproses dan dikirim ke {topic_channel}")

        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self, broker_name="bevywise"):
        broker = BROKERS.get(broker_name, BROKERS["bevywise"])
        print(f"Menghubungkan ke broker {broker_name} ({broker['url']}:{broker['port']})...")
        self.client.connect(broker["url"], broker["port"], 60)
        self.client.loop_forever()

if __name__ == "__main__":
    server = MQTTServer()
    server.start(broker_name="bevywise")