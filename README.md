# MQTT Topic Detection with KeyBERT
Deteksi topik percakapan real-time menggunakan KeyBERT dan MQTT.

## Deskripsi Umum
Proyek ini merupakan aplikasi chat berbasis topik yang memungkinkan pengguna untuk mengirim dan menerima pesan melalui MQTT (Message Queuing Telemetry Transport), protokol ringan yang umum digunakan dalam sistem komunikasi. Setiap pesan yang dikirim akan diproses oleh server untuk mendeteksi topik menggunakan model NLP berbasis KeyBERT. Topik yang terdeteksi akan digunakan untuk mendistribusikan pesan hanya kepada klien yang berlangganan (subscribe) ke topik tersebut, sehingga percakapan menjadi lebih terorganisir dan relevan.

## Cara Menjalankan
1. Install dependencies:
   pip install -r requirements.txt
   
2. Jalankan server: 
    python server.py

3. Jalankan klien (di terminal terpisah):
    python client_ui_1.py
    python client_ui_2.py

## Struktur Topik MQTT
- chat/messages – Saluran umum untuk semua pesan masuk dari klien ke server.
- chat/response – (opsional) Untuk pesan hasil proses yang dapat digunakan debugging.
- topic/<nama_topik> – Saluran dinamis sesuai topik terdeteksi (misalnya: topic/kesehatan).