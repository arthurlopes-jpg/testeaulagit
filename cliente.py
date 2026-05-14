import socket
import cv2
import numpy as np

class Cliente():
    """
    Classe Cliente - API Socket
    """
    def __init__(self, server_ip, port):
        """
        Construtor da classe Cliente
        """
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
    def start(self):
        """
        Método que inicializa a execução do Cliente
        """
        endpoint = (self.__server_ip,self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Conexão realizada com sucesso!")
            self.__method()
        except:
            print("Servidor não disponível")

    
    def __method(self):
        try:
            # 1. Carrega a imagem local
            img = cv2.imread('faces/image_0001.jpg')
            if img is None:
                print("Erro: Arquivo 'image.png' não encontrado!")
                return

            # 2. Codifica para bytes (conforme image_6.png)
            _, img_encoded = cv2.imencode('.jpg', img)
            img_bytes = bytes(img_encoded)
            
            tamanho_da_imagem_codificado = len(img_bytes).to_bytes(4, 'big')
           
            self.__tcp.send(tamanho_da_imagem_codificado)
            self.__tcp.send(img_bytes)
        

            # 5. RECEBE O TAMANHO DA IMAGEM PROCESSADA
            tam_proc = int(self.__tcp.recv(1024).decode('ascii'))
    

            # 6. RECEBE A IMAGEM PROCESSADA EM BLOCOS
            dados_final = b""
            while len(dados_final) < tam_proc:
                bloco = self.__tcp.recv(4096)
                if not bloco: break
                dados_final += bloco

            # 7. MOSTRA A IMAGEM (Requisito da image_4.png)
            img_final = cv2.imdecode(np.frombuffer(dados_final, np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Resultado - Deteccao Facial', img_final)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            self.__tcp.close()
        except Exception as e:
            print("Erro no cliente:", e)