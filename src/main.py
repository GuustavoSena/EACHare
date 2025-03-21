import os
import sys
import socket

from peer_manager import PeerManager
from server import iniciar_servidor
from clock import Clock

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


def carregar_peers(arquivo, peer_manager):
    if not os.path.isfile(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        sys.exit(1)

    with open(arquivo, 'r') as f:
        for linha in f:
            peer = linha.strip()
            if peer:
                peer_manager.adicionar_peer(peer)


def preparar_socket(endereco_porta):
    endereco, porta = endereco_porta.split(":")
    porta = int(porta)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((endereco, porta))
    sock.listen()
    return sock


def enviar_mensagem(peer, mensagem):
    endereco, porta = peer.split(":")
    porta = int(porta)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((endereco, porta))
            s.sendall(mensagem.encode())
            print(f"Encaminhando mensagem \"{mensagem.strip()}\" para {peer}")
        return True
    except Exception as e:
        return False


def menu(peer_manager, endereco_porta, clock, diretorio):
    while True:
        print("\nEscolha um comando:")
        print("[1] Listar peers")
        print("[9] Sair")
        opcao = input("> ")

        if opcao == "1":
            peers = peer_manager.listar_peers()
            print("\nLista de peers:")
            print("[0] voltar para o menu anterior")
            for i, peer in enumerate(peers, 1):
                print(f"[{i}] {peer.endereco_porta} {peer.status}")
            escolha = input("\n> ")

            if escolha == "0":
                continue

            try:
                index = int(escolha) - 1
                peer_escolhido = peers[index]
            except:
                print("Escolha inválida.")
                continue

            clock.incrementar()
            msg = f"{endereco_porta} {clock.valor} HELLO\n"
            sucesso = enviar_mensagem(peer_escolhido.endereco_porta, msg)

            novo_status = "ONLINE" if sucesso else "OFFLINE"
            peer_manager.atualizar_status(peer_escolhido.endereco_porta, novo_status)

        elif opcao == "2":
            peers = peer_manager.listar_peers()
            for peer in peers:
                clock.incrementar()
                msg = f"{endereco_porta} {clock.valor} GET_PEERS\n"
                sucesso = enviar_mensagem(peer.endereco_porta, msg)

                novo_status = "ONLINE" if sucesso else "OFFLINE"
                peer_manager.atualizar_status(peer.endereco_porta, novo_status)

        elif opcao == "3":
            print("\nArquivos compartilhados:")
            try:
                arquivos = os.listdir(diretorio)
                if arquivos:
                    for nome in arquivos:
                        print(nome)
                else:
                    print("(Nenhum arquivo encontrado)")
            except Exception as e:
                print(f"Erro ao acessar o diretório: {e}")


        elif opcao == "9":
            print("Saindo...")
            peers_online = [p for p in peer_manager.listar_peers() if p.status == "ONLINE"]
            for peer in peers_online:
                clock.incrementar()
                msg = f"{endereco_porta} {clock.valor} BYE\n"
                enviar_mensagem(peer.endereco_porta, msg)
            break


        else:
            print("Opção inválida.")


def main():
    endereco_porta, arquivo_peers, diretorio = validar_entrada()
    peer_manager = PeerManager()
    clock = Clock()

    carregar_peers(arquivo_peers, peer_manager)
    sock = preparar_socket(endereco_porta)
    iniciar_servidor(sock, peer_manager, clock, endereco_porta)

    print("\nSocket criado com sucesso! Aguardando conexões...\n")

    menu(peer_manager, endereco_porta, clock, diretorio)


if __name__ == "__main__":
    main()
