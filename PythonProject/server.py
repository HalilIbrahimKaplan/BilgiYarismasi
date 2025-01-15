import socket
import os
import time

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Sunucu başlatıldı, istemciden gelen bağlantıyı bekliyoruz...")

client_socket, client_address = server_socket.accept()
print(f"Bağlantı kabul edildi: {client_address}")

client_socket.sendall("Yarışmaya hoş geldiniz! Başlamak için 'basla' yazın.".encode('utf-8'))

try:
    request = client_socket.recv(1024).decode('utf-8')
    if request.lower() == "basla":
        client_socket.sendall("Yarışma başlıyor!".encode('utf-8'))

        score = 0
        for i in range(1, 6):  # 5 soru örneği
            question_file = os.path.join("sorular_ve_cevaplar", f"soru_{i}.txt")
            answer_file = os.path.join("sorular_ve_cevaplar", f"cevap_{i}.txt")

            with open(question_file, 'r', encoding='utf-8') as q_file:
                question = q_file.read().strip()

            with open(answer_file, 'r', encoding='utf-8') as a_file:
                answer = a_file.read().strip()

            client_socket.sendall(f"Soru {i}: {question}".encode('utf-8'))

            start_time = time.time()
            client_socket.settimeout(10)  # Cevap için 10 saniye zaman ver

            try:
                client_answer = client_socket.recv(1024).decode('utf-8')
                elapsed_time = time.time() - start_time

                if elapsed_time > 10:
                    raise socket.timeout  # Süre aşıldıysa bir timeout hatası simüle et

                if client_answer.lower() == answer.lower():
                    score += 10
                    client_socket.sendall(f"Tebrikler! Cevabınız doğru. Puanınız: {score}".encode('utf-8'))
                else:
                    client_socket.sendall(f"Yanlış cevap! Doğru cevap: {answer}. Puanınız: {score}".encode('utf-8'))
                    break  # Yanlış cevap verildiğinde yarışmayı bitir
            except socket.timeout:
                client_socket.sendall(f"Süre doldu! Yarışma sona eriyor. Toplam puanınız: {score}".encode('utf-8'))
                break

        client_socket.sendall(f"Yarışma sona erdi. Toplam puanınız: {score}. Programdan çıkılıyor.".encode('utf-8'))
        time.sleep(1)  # Mesajın istemciye ulaşması için bekle
    else:
        client_socket.sendall("Geçersiz komut, programdan çıkılıyor.".encode('utf-8'))

finally:
    print("\nBağlantı kapatılıyor...")
    client_socket.close()
    server_socket.close()
