# Constants for HiveMQ and Mosquitto
BROKERS = {
    "emqx": {"url": "broker.emqx.io", "port": 1883},
    "bevywise": {"url": "public-mqtt-broker.bevywise.com", "port": 1883}
}

TOPICS = {
    "messages": "chat/messages",       # Untuk mengirim pesan
    "response": "chat/response",       # Untuk menerima pesan
    "topics": "chat/topics"            # Khusus hasil deteksi topik
}   

