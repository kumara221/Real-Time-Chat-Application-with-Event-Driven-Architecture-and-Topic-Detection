import paho.mqtt.client as mqtt
import re
import time
import json
from sentiment import is_sentiment

# Function to detect negative sentiment
def is_sentiment(message):
    negative_keywords = [
        "idiot", "stupid", "loser", "dumb", "moron", "asshole", "jerk", "bastard", "dick",
        "crap", "freak", "bitch", "shithead", "damn", "fuck", "bodoh", "tolol", "goblok",
        "bangsat", "anjing", "kampret", "bajingan", "setan", "tai",
        "bego", "keparat", "brengsek", "sialan"
    ]
    clean_message = re.sub(r'\W', ' ', message.lower())

    # Check if any negative keyword is present
    if any(word in clean_message for word in negative_keywords):
        return "negative"
    else:
        return "positive"


def on_connect(client, userdata, flags, rc):
    print(f"Server connected with result code {rc}")
    client.subscribe("chat/messages")  # Subscribe to incoming messages


def on_message(client, userdata, msg):
    # Decode the received message
    message = msg.payload.decode('utf-8')

    # Parse the JSON message to extract the sent time and content
    try:
        message_data = json.loads(message)
        content = message_data.get("message")
        sent_time = message_data.get("sent_time")
        print(f"Received message: {content}")

    except json.JSONDecodeError:
        print("Error decoding the message.")
        return

    if sent_time:
        # Calculate the latency (time from sending to receiving the message)
        received_time = time.time()
        latency = received_time - sent_time
        print(f"Latency: {latency:.4f} seconds")

        # Sentiment detection logic
        sentiment_result = is_sentiment(message)
        sentiment_response = f"{sentiment_result.capitalize()} sentiment detected."

        # Relay message along with sentiment analysis
        relayed_message = f"{content} | Sentiment: {sentiment_response}"
        print(f"Relaying message: {relayed_message}")

        if sentiment_result == 'negative':
            new_message = re.sub(r'(?<=: ).+', lambda m: '*' *
                                 len(m.group()), message)
            relayed_message = f"{new_message} | Sentiment: {sentiment_response}"
            client.publish("chat/response", relayed_message)
        else:
            client.publish("chat/response", content)


# Initialize MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to local broker (localhost)
client.connect("localhost", 1883, 60)

# Start the loop to listen for messages
client.loop_forever()
