from flask import Flask, render_template, request, Response
import socket

from translate_main_console import listCodeLangs

# pip install Flask
app = Flask(__name__, template_folder='src')

clientes = []


@app.route('/')
def index():
    return render_template('./index.html', array=listCodeLangs(), opcao=None)


@app.route('/translate', methods=['POST'])
def traduzir():
    text_web = request.form['texto']
    opcao = request.form['opcao']

    data = opcao.split(':')
    codigo = data[0]

    host = 'SERVER_IP'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            dest_lang = codigo
            requestTranslate = f"{text_web}|{dest_lang}"
            client_socket.sendall(requestTranslate.encode('utf-8'))
            resultado: str = client_socket.recv(1024).decode('utf-8')
        except Exception as e:
            print("Erro:", e)
        finally:
            client_socket.close()

    return render_template('./index.html', resultado=resultado,
                           text=text_web, opcao=opcao, array=listCodeLangs())


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
