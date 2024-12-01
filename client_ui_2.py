import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import scrolledtext
import time
import json
from const import BROKERS


class MQTTClientApp:
    def __init__(self, root, client_name, broker="localhost", port=1883):
        self.client_name = client_name
        self.root = root
        self.root.title(f"{self.client_name} - MQTT Chat Client")

        # Setup MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker, port, 60)

        # UI Elements
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state="disabled", height=20)
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.message_input = tk.Entry(root, width=50)
        self.message_input.grid(row=1, column=0, padx=10, pady=10)
        self.message_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Start MQTT loop
        self.client.loop_start()

        # Time tracking for latency calculation
        self.sent_time = None  # Time when the message is sent

    def on_connect(self, client, userdata, flags, rc):
        self.display_message(
            f"{self.client_name} connected to MQTT broker (result code: {rc})")
        self.client.subscribe("chat/response")  # Listen for relayed messages

    def on_message(self, client, userdata, msg):
        response = msg.payload.decode('utf-8')
        # Display all messages except those sent by this client
        if not response.startswith(f"{self.client_name}:"):
            self.display_message(response)

    def send_message(self, event=None):
        message = self.message_input.get()
        if message.strip():
            self.sent_time = time.time()  # Record the time when the message is sent
            full_message = {
                "message": f"{self.client_name}: {message}",
                "sent_time": self.sent_time
            }
            # Send the message with sent_time to server
            self.client.publish("chat/messages", json.dumps(full_message))
            self.display_message(f"[You] {message}")
            self.message_input.delete(0, tk.END)

    def display_message(self, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(tk.END)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    broker_choice = "mosquitto"
    broker = BROKERS[broker_choice]
    app = MQTTClientApp(root, client_name="Klien 2",
                        broker=broker['url'], port=1883)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
