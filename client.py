import threading
import socket
import hashlib
import logging

logging.basicConfig(level=logging.INFO)

def sendMessage(conn):
    try:
        while True:
            message = input('Ingresa peticion al servidor: ')
            if message.lower() == 'q':
                conn.close()
                break
            conn.sendall(message.encode("utf-8"))
    except Exception as e:
        logging.error(f"Error al enviar peticion al servidor: {e}")
    finally:
        conn.close()

def recvMessage(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            logging.info(f"Peticion del servidor recivida: {data.decode('utf-8')}")
    except Exception as e:
        logging.error(f"Error al recivir peticion del servidor: {e}")
    finally:
        conn.close()

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        addr = ('', 8000)
        sock.connect(addr)
        flag = threading.Event()
        
        while True:
            server_addr = sock.getpeername()
            logging.info(f'conectado al servidor {server_addr} ...')
            threading.Thread(target=sendMessage, args=(sock, flag)).start()
            threading.Thread(target=recvMessage, args=(sock, flag)).start()

if __name__ == "__main__":
    start()