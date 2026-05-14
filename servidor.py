import socket
import cv2
import numpy as np
import os

class Servidor():
    """
    Classe Servidor - API Socket
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(1)
            print("Servidor iniciado em ", self._host, ": ", self._port)
            while True:
                con, client = self.__tcp.accept()
                self._service(con, client)
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        print("Atendendo:", client)
        try:
            # 1. tamanho
            msg = con.recv(1024)
            tam = int.from_bytes(msg, 'big')
         

            # 2. protocolo
            dados_bytes = b""
            while len(dados_bytes) < tam:
                bloco = con.recv(4096)
                if not bloco: break
                dados_bytes += bloco

            # 3. decodifica proc inverso
            img = cv2.imdecode(np.frombuffer(dados_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            # Localiza o classificador (ajustado para Windows/Linux)
            xml_path = os.path.join(os.path.dirname(cv2.__file__), 'data', 'haarcascade_frontalface_default.xml')
            face_cascade = cv2.CascadeClassifier(xml_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Desenha retângulo AZUL (255, 0, 0) conforme image_4.png
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # 4. CODIFICA PARA ENVIAR DE VOLTA
            _, img_proc_encoded = cv2.imencode('.jpg', img)
            resp_bytes = bytes(img_proc_encoded)
            tam_resp = len(resp_bytes)

            con.send(str(tam_resp).encode('ascii'))
            con.send(resp_bytes)
            print(f"Sucesso: Face detectada e enviada para {client}")

        except Exception as e:
            print("Erro no servidor:", e)
        finally:
            con.close()
