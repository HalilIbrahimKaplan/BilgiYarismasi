import socket

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

try:
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Sunucudan gelen mesaj: {message}\n")

    start_command = input("Yarışmaya başlamak için 'basla' yazın: ")
    client_socket.sendall(start_command.encode('utf-8'))

    if start_command.lower() != "basla":
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Sunucudan gelen mesaj: {response}")
        raise SystemExit  # Programı sonlandır

    while True:
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Sunucudan gelen mesaj: {response}\n")

        if "Programdan çıkılıyor" in response or "Yarışma sona erdi" in response:
            break

        if "Soru" in response:
            user_answer = input("Cevabınızı girin (Süre 10 sn): ")
            client_socket.sendall(user_answer.encode('utf-8'))

except ConnectionResetError:
    print("\nSunucu bağlantıyı kapattı.")
except BrokenPipeError:
    print("\nBağlantı beklenenden önce kesildi.")
finally:
    print("\nBağlantı kapatılıyor...")
    client_socket.close()
