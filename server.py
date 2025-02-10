import threading
import socket
import hashlib
import logging

logging.basicConfig(level=logging.INFO)

def sendMessage(conn, flag):
    try:
        while True:
            message = input('Ingresa peticion al cliente: ')
            if message.lower() == 'q':
                conn.close()
                break
            conn.send(message.encode("utf-8"))
    except Exception as e:
        logging.error(f"Error al enviar peticion al cliente: {e}")
    finally:
        conn.close()

def recvMessage(conn, flag):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            logging.info(f"Peticion del cliente recivida: {data.decode("utf-8")}")
    except Exception as e:
        logging.error(f"Error al recivir peticion del cliente: {e}")
    finally:
        conn.close()

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0, fileno=None) as sock:
        sock.bind(('', 8000))
        sock.listen(1)
        flag = threading.Event()
        
        while True:
            conn, addr = sock.accept()
            logging.info(f'{addr} conectado al servidor...')
            threading.Thread(target=sendMessage, args=(conn, flag)).start()
            threading.Thread(target=recvMessage, args=(conn, flag)).start()
    
if __name__ == "__main__":
    start()