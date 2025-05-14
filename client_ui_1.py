import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import scrolledtext, ttk
import json
from const import BROKERS, TOPICS

class ChatClient:
    def __init__(self, root, client_name, broker_name="emqx"):
        self.client_name = client_name
        self.root = root
        self.root.title(f"{client_name} - Pengirim Pesan")
        
        # Setup MQTT
        self.broker = BROKERS[broker_name]
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(self.broker["url"], self.broker["port"], 60)
        
        # UI Setup
        self.setup_ui()
        self.client.loop_start()

    def setup_ui(self):
        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", width=60, height=15
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Message Input
        self.message_entry = ttk.Entry(self.root, width=50)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Send Button
        self.send_button = ttk.Button(self.root, text="Kirim", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(TOPICS["response"])
        self.add_message(f"[SISTEM] Terhubung ke broker {self.broker['url']}")

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

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root, "Client_1", broker_name="bevywise")
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()