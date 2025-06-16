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
        if rc == 0:
            print("Server connected to MQTT broker.")
            client.subscribe(TOPICS["messages"])
            print(f"Subscribed to: {TOPICS['messages']}")
        else:
            print(f"Connection failed (RC: {rc})")

    def on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode()
            print(f"\n📥 Pesan diterima: {msg.topic} - {payload_str}")
            data = json.loads(payload_str)

            sender = data.get("sender")
            message = data.get("message")

            if not sender or not message:
                print("Payload tidak lengkap, diabaikan.")
                return

            topics = extract_topic(message)
            print(f"Topik terdeteksi: {topics}")

            if not topics:
                print("Tidak ada topik terdeteksi, pesan tidak dikirim.")
                return

            for topic in topics:
                topic_channel = f"topic/{topic.lower()}"
                client.publish(topic_channel, json.dumps({
                    "sender": sender,
                    "message": message,
                    "topics": topics,
                    "processed": True
                }))
                print(f"Pesan dipublish ke: {topic_channel}")

            print(f"Pesan selesai diproses dari {sender}.")

        except Exception as e:
            print(f"Error: {e}")

    def start(self, broker_name="bevywise"):
        broker = BROKERS.get(broker_name, BROKERS["bevywise"])
        print(f"🔌 Menghubungkan ke broker {broker_name} ({broker['url']}:{broker['port']})...")
        self.client.connect(broker["url"], broker["port"], 60)
        self.client.loop_forever()

if __name__ == "__main__":
    server = MQTTServer()
    server.start(broker_name="bevywise")