import socket
import threading
from googletrans import Translator


# pip install googletrans==3.1.0a0
def translate_text(text, dest_lang):
    try:
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_lang)
        return translated_text.text
    except ConnectionError:
        return "Ops...!:", "Erro na chamada da API!"


def handle_client(client_socket, client_address):
    try:
        with client_socket:
            print('Conexão de', client_address)
            data = client_socket.recv(1024).decode('utf-8')
            data = data.split('|')
            if len(data) == 2:
                text, dest_lang = data
                translated_text = translate_text(text, dest_lang)
                client_socket.sendall(translated_text.encode('utf-8'))
            else:
                client_socket.sendall("Requisição inválida!".encode('utf-8'))
    except ConnectionResetError:
        print(f"Conexão perdida com {client_address}")
    finally:
        client_socket.close()
        print(f"Conexão encerrada com {client_address}")


def main():
    host = '0.0.0.0'
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(8)

        print("Servidor ouvindo na porta", port)

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
        except KeyboardInterrupt:
            print("Servidor encerrado")
        finally:
            server_socket.close()


if __name__ == "__main__":
    main()
