import socket

def tratar_mensagem(mensagem, peer_manager, clock, endereco_proprio):
    partes = mensagem.split()
    if len(partes) < 3:
        print("Mensagem mal formatada.")
        return

    origem = partes[0]
    tipo = partes[2]
    clock.atualizar_ao_receber()

    if tipo == "HELLO":
        peer_manager.adicionar_peer(origem, status="ONLINE")

    elif tipo == "GET_PEERS":
        peer_manager.adicionar_peer(origem, status="ONLINE")

        peers = peer_manager.listar_peers()
        peers_excluindo_origem = [p for p in peers if p.endereco_porta != origem]

        resposta_args = []
        for peer in peers_excluindo_origem:
            linha = f"{peer.endereco_porta}:{peer.status}:0"
            resposta_args.append(linha)

        total = len(resposta_args)
        resposta = f"{endereco_proprio} {clock.valor} PEER_LIST {total} " + " ".join(resposta_args) + "\n"

        endereco, porta = origem.split(":")
        porta = int(porta)

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((endereco, porta))
                s.sendall(resposta.encode())
                print(f"Encaminhando mensagem \"{resposta.strip()}\" para {origem}")
        except Exception as e:
            print(f"Erro ao enviar PEER_LIST: {e}")

    elif tipo == "PEER_LIST":
        qtd_peers = int(partes[3])
        novos_peers = partes[4:]
        for p in novos_peers:
            try:
                endereco, status, _ = p.rsplit(":", 2)
                peer_manager.adicionar_peer(endereco, status=status)
            except Exception as e:
                print(f"Erro ao processar peer da lista: {p} -> {e}")
            
    elif tipo == "BYE":
        peer_manager.atualizar_status(origem, status="OFFLINE")

