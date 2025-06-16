import paho.mqtt.client as mqtt
import tkinter as tk
from tkinter import scrolledtext, ttk
import json
from const import BROKERS

TOPIC_OPTIONS = ["kesehatan", "politik", "pendidikan"]

class ChatClient:
    def __init__(self, root, client_name, broker_name="emqx"):
        self.client_name = client_name
        self.root = root
        self.root.title(f"{client_name} - Pilih Topik")

        self.broker = BROKERS[broker_name]
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.selected_topic = tk.StringVar(value=TOPIC_OPTIONS[0])

        self.create_topic_selection_ui()

    def create_topic_selection_ui(self):
        label = ttk.Label(self.root, text="Pilih Topik:")
        label.pack(padx=10, pady=5)

        dropdown = ttk.Combobox(self.root, values=TOPIC_OPTIONS, textvariable=self.selected_topic, state="readonly")
        dropdown.pack(padx=10, pady=5)

        join_button = ttk.Button(self.root, text="Gabung", command=self.start_chat)
        join_button.pack(padx=10, pady=10)

    def start_chat(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"{self.client_name} - Topik: {self.selected_topic.get()}")
        self.setup_ui()

        self.client.connect(self.broker["url"], self.broker["port"], 60)
        self.client.loop_start()

    def setup_ui(self):
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled", width=60, height=15
        )
        self.chat_display.pack(padx=10, pady=10)

        self.message_entry = ttk.Entry(self.root, width=50)
        self.message_entry.pack(padx=10, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = ttk.Button(self.root, text="Kirim", command=self.send_message)
        self.send_button.pack(padx=10, pady=5)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            topic = f"topic/{self.selected_topic.get()}"
            client.subscribe(topic)
            print(f"Terhubung ke broker. Subscribed ke topik: {topic}")
        else:
            print(f"Gagal terhubung, kode: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            sender = payload.get("sender", "Unknown")
            message = payload.get("message", "")
            topics = payload.get("topics", [])
            processed = payload.get("processed", False)

            if not processed:
                return

            display_sender = "Anda" if sender == self.client_name else sender
            display_message = (
                f"{display_sender}: {message}\n\n[Topik Terdeteksi: {', '.join(repr(t) for t in topics)}]"
            )

            self.add_message(display_message)

        except json.JSONDecodeError:
            print("Gagal decode pesan")
            
    def send_message(self, event=None):
        message = self.message_entry.get()
        if message.strip():
            payload = {
                "sender": self.client_name,
                "message": message
            }

            topic = f"topic/{self.selected_topic.get()}"
            self.client.publish(topic, json.dumps(payload))
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

    window_width = 500
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    app = ChatClient(root, "Client_1", broker_name="bevywise")
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()