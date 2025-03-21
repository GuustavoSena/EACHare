import os
import sys
import socket

def validar_entrada():
    if len(sys.argv) != 4:
        print("Uso: python main.py <endereco>:<porta> <vizinhos.txt> <diretorio_compartilhado>")
        sys.exit(1)

    endereco_porta = sys.argv[1]
    arquivo_peers = sys.argv[2]
    diretorio = sys.argv[3]

    if not os.path.isdir(diretorio):
        print(f"Erro: O diretório '{diretorio}' não é válido ou não pode ser lido.")
        sys.exit(1)

    return endereco_porta, arquivo_peers, diretorio


def carregar_peers(arquivo):
    peers = []
    if not os.path.isfile(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        sys.exit(1)

    with open(arquivo, 'r') as f:
        for linha in f:
            peer = linha.strip()
            if peer:
                peers.append((peer, 'OFFLINE'))
                print(f"Adicionando novo peer {peer} status OFFLINE")
    return peers


def preparar_socket(endereco_porta):
    endereco, porta = endereco_porta.split(":")
    porta = int(porta)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((endereco, porta))
    sock.listen()
    return sock


def main():
    endereco_porta, arquivo_peers, diretorio = validar_entrada()
    peers = carregar_peers(arquivo_peers)
    sock = preparar_socket(endereco_porta)

    print("\nSocket criado com sucesso! Aguardando conexões...\n")
    # Aqui no futuro virá a lógica para escutar conexões e mostrar o menu

if __name__ == "__main__":
    main()
