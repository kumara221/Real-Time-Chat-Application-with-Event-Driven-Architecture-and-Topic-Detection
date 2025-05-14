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
        client.subscribe(TOPICS["messages"])

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            sender = data["sender"]
            message = data["message"]
            
            # Deteksi topik
            topics = extract_topic(message)
            topic_info = f"Topik dari {sender}: {', '.join(topics)}"
            
            # Kirim pesan asli ke semua client
            client.publish(TOPICS["response"], json.dumps({
                "sender": sender,
                "message": message
            }))
            
            # Kirim info topik HANYA ke client lawan
            client.publish(TOPICS["topics"], json.dumps({
                "target": "client_2" if sender == "client_1" else "client_1",
                "topics": topic_info
            }))
            
            print(f"Pesan diproses: {sender} -> {message} | Topik: {topics}")
            
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