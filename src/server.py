import threading
import socket
from handler import tratar_mensagem

def tratar_conexao(conn, addr, peer_manager, clock, endereco_proprio):
    try:
        data = conn.recv(1024).decode()
        if data:
            print(f"Mensagem recebida: \"{data.strip()}\"")
            tratar_mensagem(data.strip(), peer_manager, clock, endereco_proprio)
    except Exception as e:
        print(f"[Erro ao tratar conexão] {e}")
    finally:
        conn.close()


def iniciar_servidor(sock, peer_manager, clock, endereco_proprio):
    def escutar():
        while True:
            try:
                conn, addr = sock.accept()
                thread = threading.Thread(
                    target=tratar_conexao,
                    args=(conn, addr, peer_manager, clock, endereco_proprio),
                    daemon=True
                )
                thread.start()
            except Exception as e:
                print(f"[Erro servidor] {e}")
                continue

    t = threading.Thread(target=escutar, daemon=True)
    t.start()
