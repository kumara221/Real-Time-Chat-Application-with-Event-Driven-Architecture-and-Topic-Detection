import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import scrolledtext, ttk, font
import json
from const import BROKERS, TOPICS

class ChatClientWithTopics:
    def __init__(self, root, client_name, broker_name="emqx"):
        self.client_name = client_name
        self.root = root
        self.root.title(f"{client_name} - Penerima Pesan + Deteksi Topik")
        
        # Setup MQTT
        self.broker = BROKERS[broker_name]
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker["url"], self.broker["port"], 60)
        
        # UI Setup
        self.setup_ui()
        self.client.loop_start()

    def setup_ui(self):
        # Font Configuration
        bold_font = font.Font(weight="bold")
        
        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", width=60, height=15
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Topic Display
        self.topic_frame = ttk.LabelFrame(self.root, text="Deteksi Topik")
        self.topic_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.topic_display = scrolledtext.ScrolledText(
            self.topic_frame, wrap=tk.WORD, state="disabled", width=60, height=5
        )
        self.topic_display.pack(padx=5, pady=5)
        self.topic_display.tag_config("topic", foreground="blue", font=bold_font)
        
        # Message Input
        self.message_entry = ttk.Entry(self.root, width=50)
        self.message_entry.grid(row=2, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Send Button
        self.send_button = ttk.Button(self.root, text="Balas", command=self.send_message)
        self.send_button.grid(row=2, column=1, padx=10, pady=10)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(TOPICS["response"])
        self.client.subscribe(TOPICS["topics"])
        self.add_message(f"[SISTEM] Terhubung ke broker {self.broker['url']}")

    def on_message(self, client, userdata, msg):
        data = json.loads(msg.payload.decode())
        
        if msg.topic == TOPICS["response"]:
            if data["sender"] != self.client_name:
                self.add_message(f"{data['sender']}: {data['message']}")
        elif msg.topic == TOPICS["topics"]:
            if data["target"] == self.client_name:
                self.show_topic(data["topics"])

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip():
            payload = {
                "sender": self.client_name,
                "message": message
            }
            self.client.publish(TOPICS["messages"], json.dumps(payload))
            self.add_message(f"Anda: {message}", is_user=True)
            self.message_entry.delete(0, tk.END)

    def add_message(self, message, is_user=False):
        self.chat_display.config(state="normal")
        tag = "user" if is_user else None
        self.chat_display.insert(tk.END, f"{message}\n", tag)
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def show_topic(self, topic_info):
        self.topic_display.config(state="normal")
        self.topic_display.insert(tk.END, f"⚡ {topic_info}\n", "topic")
        self.topic_display.config(state="disabled")
        self.topic_display.see(tk.END)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClientWithTopics(root, "Client_2", broker_name="bevywise")
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()