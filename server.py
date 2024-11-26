import paho.mqtt.client as mqtt
import re

# Function to detect negative sentiment


def is_sentiment(message):
    negative_keywords = [
        "idiot", "stupid", "loser", "dumb", "moron", "asshole", "jerk", "bastard", "dick",
        "crap", "freak", "bitch", "shithead", "damn", "fuck", "bodoh", "tolol", "goblok",
        "bangsat", "anjing", "kampret", "bajingan", "setan", "tai", "jancok", "monyet",
        "bego", "keparat", "brengsek", "sialan", "kontol", "memek", "asu", "cuki", "puki"
    ]
    clean_message = re.sub(r'\W', ' ', message.lower())
    return any(word in clean_message for word in negative_keywords)

# Callback when connected to broker


def on_connect(client, userdata, flags, rc):
    print(f"Server connected with result code {rc}")
    client.subscribe("chat/messages")  # Subscribe to incoming messages

# Callback when a message is received


def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    print(f"Received message: {message}")

    # Sentiment detection logic
    sentiment_detected = False
    sentiment_response = "Message received successfully."
    if is_sentiment(message):
        sentiment_response = "Negative sentiment detected."
        sentiment_detected = True

    # Relay message along with sentiment analysis
    relayed_message = f"{message} | Sentiment: {sentiment_response}"
    print(f"Relaying message: {relayed_message}")

    if sentiment_detected:
        client.publish("chat/sentiment", "Pesan mengandung sentimen negatif")
    else:
        client.publish("chat/response", relayed_message)


# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to HiveMQ broker
client.connect("broker.hivemq.com", 1883, 60)

# Start the loop to listen for messages
client.loop_forever()
